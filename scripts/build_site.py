"""
Phase 3 - build the interactive network map as a static page.

Renders index.html from db/graph.db. The layout is computed here in Python with
a fixed seed and written into the SVG as coordinates, so the page is identical
on every build and carries no layout library.

Design note. A force-directed drawing of the whole graph would be a hairball
that hides the central finding. The graph is in seventeen disconnected pieces,
so the page draws seventeen small multiples: the fragmentation becomes the thing
you see first rather than something the caption has to explain away.

Colour carries three categories only - the failed institution, a named
counterparty, and a party the Bank of Ghana described but did not name. That is
the distinction the whole project turns on, and three slots is also what the
palette validates for small multiples. Everything finer (holding company,
person, group) is carried by node shape, and every node is directly labelled,
which is required anyway because the third slot sits below 3:1 contrast on the
light surface.

Usage:  python scripts/build_site.py
"""

import html
import json
import math
import sqlite3
import sys
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyse_graph import DB, load_graph  # noqa: E402
from site_template import SCRIPT, STYLE  # noqa: E402

OUT = ROOT / "index.html"

PANEL_W, PANEL_H = 300, 190
CASE_W, CASE_H = 620, 380


def short_name(name, entity_type):
    """Display label. Long placeholder names are unreadable at panel scale."""
    if name.startswith("UNNAMED "):
        s = name[len("UNNAMED "):]
        for cut in (" of ", " in the "):
            if cut in s:
                s = s.split(cut)[0]
                break
        return s
    # Only the legal form and the "savings and loans" tail, which every one of
    # the 23 carries. Trimming "Finance" too turned Ideal Finance Limited into
    # "Ideal" in a panel that also holds Ideal Capital Partners, Ideal Trade and
    # Ideal Bottling, where the label has to say which one it is.
    for suffix in (" Savings and Loans Company Limited", " Savings and Loans Limited",
                   " Savings and Loans Ltd.", " Company Limited",
                   " Limited", " Ltd."):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return name


def colour_slot(node):
    """1 = the failed institution, 2 = named counterparty, 3 = unnamed party."""
    if node["scope_class"] == "core_23":
        return 1
    return 3 if not node["is_named"] else 2


def shape_for(entity_type):
    return {"institution": "circle", "holding_company": "square",
            "corporate_entity": "rounded", "person": "diamond",
            "placeholder_group": "ring"}.get(entity_type, "circle")


def layout(g, nodes, width, height, pad=54):
    """Deterministic positions. Stars get a radial layout; the rest a seeded spring.

    Node order is fixed by sorting: a set's iteration order varies between
    processes, and spring_layout consumes that order, so without this the page
    would differ from one build to the next.
    """
    nodes = sorted(nodes)
    sub = nx.Graph()
    sub.add_nodes_from(nodes)
    sub.add_edges_from((u, v) for u, v in nx.Graph(g).edges(nodes) if u in nodes and v in nodes)
    n = sub.number_of_nodes()
    inner_w, inner_h = width - 2 * pad, height - 2 * pad

    if n == 1:
        return {list(nodes)[0]: (width / 2, height / 2)}
    if n == 2:
        a, b = sorted(nodes)
        return {a: (pad, height / 2), b: (width - pad, height / 2)}

    degrees = dict(sub.degree())
    hub = max(degrees, key=lambda k: (degrees[k], k))
    if degrees[hub] == n - 1:  # a star: hub in the middle, leaves around it
        others = sorted(k for k in nodes if k != hub)
        radius_x, radius_y = inner_w * 0.40, inner_h * 0.40
        pos = {hub: (width / 2, height / 2)}
        for i, node in enumerate(others):
            angle = -math.pi / 2 + 2 * math.pi * i / len(others)
            pos[node] = (width / 2 + radius_x * math.cos(angle),
                         height / 2 + radius_y * math.sin(angle))
        return pos

    raw = nx.spring_layout(sub, seed=7, iterations=400)
    xs = [p[0] for p in raw.values()]
    ys = [p[1] for p in raw.values()]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    sx = inner_w / (x1 - x0) if x1 > x0 else 0
    sy = inner_h / (y1 - y0) if y1 > y0 else 0
    return {k: (pad + (p[0] - x0) * sx, pad + (p[1] - y0) * sy) for k, p in raw.items()}


def node_mark(x, y, slot, shape, r=9):
    """SVG for one node. Shape is the secondary encoding for the finer type."""
    fill = f"var(--series-{slot})"
    common = (f'fill="{fill}" stroke="var(--surface-1)" stroke-width="2" '
              f'vector-effect="non-scaling-stroke"')
    if shape == "square":
        return f'<rect x="{x - r:.1f}" y="{y - r:.1f}" width="{2 * r}" height="{2 * r}" {common}/>'
    if shape == "rounded":
        return (f'<rect x="{x - r:.1f}" y="{y - r:.1f}" width="{2 * r}" height="{2 * r}" '
                f'rx="3" {common}/>')
    if shape == "diamond":
        pts = f"{x:.1f},{y - r - 1:.1f} {x + r + 1:.1f},{y:.1f} {x:.1f},{y + r + 1:.1f} {x - r - 1:.1f},{y:.1f}"
        return f'<polygon points="{pts}" {common}/>'
    if shape == "ring":
        return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" '
                f'stroke="{fill}" stroke-width="3" stroke-dasharray="4 3"/>')
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" {common}/>'


def wrap(text, per_line=22, max_lines=2):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= per_line:
            cur = f"{cur} {w}".strip()
        else:
            lines.append(cur)
            cur = w
            if len(lines) == max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines and len(" ".join(lines)) < len(text):
        lines[-1] = lines[-1][:per_line - 1] + "…"
    return lines


def draw(g, nodes, width, height, evidence, label_size=10, radius=9):
    """One panel of the small multiples, or one enlarged case view."""
    nodes = sorted(nodes)
    pos = layout(g, nodes, width, height)
    edges, marks, labels = [], [], []

    for u, v, key, d in sorted(g.edges(nodes, keys=True, data=True), key=lambda e: e[2]):
        if u not in pos or v not in pos:
            continue
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        # Stop the line short of the node so the arrowhead is visible.
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy) or 1
        ox, oy = dx / dist * (radius + 6), dy / dist * (radius + 6)
        dash = "" if d["extracts_value"] else ' stroke-dasharray="3 3"'
        quote = evidence.get(key, {}).get("quote", "")
        anchor = evidence.get(key, {}).get("anchor", "")
        amount = ""
        if d["amount_value"]:
            unit = "m" if d["amount_unit"] == "million" else ""
            amount = f"{d['amount_currency']} {d['amount_value']:,.2f}{unit}"
        edges.append(
            f'<g class="edge" tabindex="0" role="button"'
            f' data-edge="{html.escape(key)}"'
            f' data-from="{html.escape(g.nodes[u]["name"])}"'
            f' data-to="{html.escape(g.nodes[v]["name"])}"'
            f' data-rel="{html.escape(d["relationship"])}"'
            f' data-amount="{html.escape(amount)}"'
            f' data-conf="{html.escape(d["confidence"])}"'
            f' data-anchor="{html.escape(anchor)}"'
            f' data-quote="{html.escape(quote)}">'
            f'<line x1="{x1 + ox:.1f}" y1="{y1 + oy:.1f}" x2="{x2 - ox:.1f}" y2="{y2 - oy:.1f}"'
            f' stroke="var(--edge)" stroke-width="2"{dash}'
            f' marker-end="url(#arrow)"/>'
            f'<line class="hit" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"'
            f' stroke="transparent" stroke-width="14"/>'
            f'</g>')

    # Node marks first, and each one is an obstacle the labels must avoid.
    blocked = []
    to_label = []
    for node in sorted(nodes):
        x, y = pos[node]
        data = g.nodes[node]
        slot = colour_slot(data)
        marks.append(node_mark(x, y, slot, shape_for(data["entity_type"]), radius))
        blocked.append((x - radius - 2, y - radius - 2, x + radius + 2, y + radius + 2))
        # In a small panel the caption already names the institution, so
        # labelling the hub as well only crowds the leaves it points at.
        if label_size <= 10 and data["scope_class"] == "core_23":
            continue
        per_line = 18 if label_size <= 10 else 26
        to_label.append((node, x, y,
                         wrap(short_name(data["name"], data["entity_type"]),
                              per_line=per_line)))

    line_h = label_size + 1

    def box_for(x, top, lines):
        half = max(len(line) for line in lines) * label_size * 0.29
        cx = min(max(x, half + 2), width - half - 2)
        return (cx - half, top - label_size, cx + half, top + (len(lines) - 1) * line_h + 2)

    def clashes(box):
        return any(not (box[2] <= o[0] or box[0] >= o[2]
                        or box[3] <= o[1] or box[1] >= o[3]) for o in blocked)

    # Placing labels one at a time against everything already placed. Without
    # this, two nodes close together in a small panel print their labels on top
    # of each other, which happened to five panels once the second regulator's
    # counterparties were added.
    for node, x, y, lines in to_label:
        above = y - radius - 7 - (len(lines) - 1) * line_h
        below = y + radius + label_size + 4
        # Preferred side first: below in the upper half of the panel, above in
        # the lower half, so a label leans away from the middle of the drawing.
        order = [below, above] if y <= height * 0.58 else [above, below]
        candidates = list(order)
        for step in range(1, 5):
            candidates += [order[0] + step * (line_h + 3) * (1 if order[0] == below else -1),
                           order[1] + step * (line_h + 3) * (1 if order[1] == below else -1)]
        top = next((t for t in candidates
                    if 2 + label_size <= t and t + (len(lines) - 1) * line_h <= height - 2
                    and not clashes(box_for(x, t, lines))), order[0])
        blocked.append(box_for(x, top, lines))
        for i, line in enumerate(lines):
            # Keep the label inside the viewBox: an outer SVG clips to its
            # viewport, so a centred label on an edge node would be cut off.
            half = len(line) * label_size * 0.29
            lx = min(max(x, half + 2), width - half - 2)
            labels.append(
                f'<text x="{lx:.1f}" y="{top + i * line_h:.1f}" '
                f'text-anchor="middle" font-size="{label_size}" '
                # Knock the label out of any edge line running behind it.
                f'paint-order="stroke" stroke="var(--surface-1)" stroke-width="3" '
                f'stroke-linejoin="round" '
                f'fill="var(--text-secondary)">{html.escape(line)}</text>')

    return (f'<svg viewBox="0 0 {width} {height}" role="img" '
            f'preserveAspectRatio="xMidYMid meet">'
            + "".join(edges) + "".join(marks) + "".join(labels) + "</svg>")


def evidence_for_edges(con):
    out = {}
    for edge_id, anchor, quote in con.execute("""
            SELECT e.edge_id, ev.anchor, ev.quote
            FROM edges e
            LEFT JOIN edge_evidence ee ON ee.edge_id = e.edge_id
            LEFT JOIN evidence ev ON ev.anchor = ee.anchor"""):
        if edge_id not in out or (anchor and not out[edge_id]["anchor"]):
            out[edge_id] = {"anchor": anchor or "", "quote": quote or ""}
    return out


def build():
    con = sqlite3.connect(DB)
    g = load_graph(con)
    evidence = evidence_for_edges(con)
    metrics = json.loads((ROOT / "docs" / "phase2" / "metrics.json").read_text(encoding="utf-8"))

    undirected = nx.Graph(g)
    components = sorted((sorted(c) for c in nx.connected_components(undirected)),
                        key=lambda c: (-len(c), sorted(g.nodes[n]["name"] for n in c)[0]))

    contested = dict(con.execute(
        "SELECT entity_id, status_note FROM entities "
        "WHERE status_note IS NOT NULL AND status_note <> ''"))

    # Case studies are keyed by a representative entity rather than by size, and
    # a component holding a contested institution is never one: the standard is
    # that contested institutions stay out of worked examples.
    cases, used = [], set()
    for key, blurb in CASE_NOTES:
        for i, comp in enumerate(components):
            if i in used or key not in comp:
                continue
            if any(n in contested for n in comp):
                continue
            cases.append((comp, blurb))
            used.add(i)
            break
    others = [c for i, c in enumerate(components) if i not in used]

    pending = metrics["verification"]["counts"].get("pending", 0)
    total_edges = sum(metrics["verification"]["counts"].values())
    shape = metrics["shape"]
    hubs_multi = len(metrics["hubs"]["connect_multiple_institutions"])

    parts = []
    parts.append(f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Related-party lending network &middot; Ghana savings &amp; loans, 2019</title>
<meta name="description" content="A network reconstruction of related-party lending behind the 23 Ghanaian savings and loans failures of 2019, built only from the Bank of Ghana revocation notice.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{STYLE}</style>
</head><body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6"
        orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" fill="var(--edge)"/></marker>
</defs></svg>
<div class="wrap">
<header>
<h1>Seventeen structures, not one network</h1>
<p class="lede">Related-party lending appears in 17 of the 23 savings &amp; loans companies
and finance houses whose licences the Bank of Ghana revoked on 16&nbsp;August&nbsp;2019. This
is what those relationships look like when two regulators&rsquo; notices are read as a graph
&mdash; including one loop that neither document shows on its own.</p>
</header>''')

    if pending:
        checked = total_edges - pending
        phrase = ("None of the" if checked == 0 else
                  f"{checked} of the")
        parts.append(f'''<div class="banner"><strong>Provisional.</strong> {phrase}
{total_edges} edges in the evidence base have been checked against the notice by hand.
Every figure on this page is provisional and is recomputed as verification is
recorded.</div>''')

    parts.append(f'''
<div class="tiles">
  <div class="tile"><div class="n">23</div><div class="k">institutions</div></div>
  <div class="tile"><div class="n">2</div><div class="k">regulators&rsquo; notices</div></div>
  <div class="tile"><div class="n">{shape['edges']}</div><div class="k">documented edges</div></div>
  <div class="tile"><div class="n">{shape['components']}</div><div class="k">separate structures</div></div>
  <div class="tile"><div class="n">{hubs_multi}</div><div class="k">entities linking two institutions</div></div>
  <div class="tile"><div class="n">{metrics["loops"]["extraction_loops"]}</div><div class="k">closed extraction loops</div></div>
</div>
<p class="section-note">Every edge restates something a regulator published. Hover or focus
any connection to read the passage behind it.</p>

<h2>What one regulator sees, and what two see</h2>
<p>Read on its own, the Bank of Ghana&rsquo;s notice shows no entity connecting two of the 23
institutions. Every counterparty it names attaches to exactly one. That is a fact about the
document: it was written to explain why each institution failed, not to map ownership across
them.</p>
<p>Adding the Securities and Exchange Commission&rsquo;s notice of 8 November 2019, which
revoked 53 fund-management licences, changes that. The Commission states what the banking
regulator had no reason to: where fund managers had placed their clients&rsquo; money.
Eleven of its 53 sections name one of the 23 institutions.</p>
<p>The clearest result needs both documents and appears in neither alone. The Bank of Ghana
records <strong>Midland</strong> as over-exposed to <strong>Liberty Asset Management</strong>;
the SEC records Liberty holding 9.45% of its funds with Midland. Each held the other, and
value moves along both arrows &mdash; the one closed extraction loop in the evidence base.</p>
<p>The graph is still in {shape['components']} pieces, and one entity now connects two
institutions where none did before. A negative result from a single source is a statement
about that source.</p>

<div class="legend">
  <span class="item"><span class="swatch" style="background:var(--series-1)"></span>failed institution</span>
  <span class="item"><span class="swatch sq" style="background:var(--series-2)"></span>named counterparty or owner</span>
  <span class="item"><span class="swatch ring"></span>party described but not named</span>
  <span class="item"><svg width="34" height="10"><line x1="1" y1="5" x2="33" y2="5" stroke="var(--edge)" stroke-width="2"/></svg>moves value out</span>
  <span class="item"><svg width="34" height="10"><line x1="1" y1="5" x2="33" y2="5" stroke="var(--edge)" stroke-width="2" stroke-dasharray="3 3"/></svg>structural only</span>
</div>
''')

    parts.append('<h2>The documented networks</h2>')
    parts.append('<p class="section-note">The largest structures in the record, each worth '
                 'reading edge by edge. A component containing a contested institution is '
                 'not shown here as a case study.</p>')
    for comp, blurb in cases:
        names = sorted(g.nodes[n]["name"] for n in comp)
        title = blurb["title"]
        parts.append(f'''<div class="case"><h3>{html.escape(title)}</h3>
<p class="section-note">{blurb["text"]}</p>
{draw(g, comp, CASE_W, CASE_H, evidence, label_size=11, radius=11)}
</div>''')

    parts.append(f'<h2>The other {len(others)}</h2>')
    parts.append('<p class="section-note">Each is an institution and the related parties the '
                 'notice attributes to it. None connects to any other panel &mdash; that '
                 'disconnection is the finding, not a drawing artefact.</p>')
    parts.append('<div class="grid">')
    for comp in others:
        inst = sorted((g.nodes[n]["name"] for n in comp
                       if g.nodes[n]["scope_class"] == "core_23"), key=len)
        cap = short_name(inst[0], "institution") if inst else "—"
        note = next((contested[n] for n in comp if n in contested), "")
        flag = (f'<div class="status"><strong>Contested.</strong> {html.escape(note)}</div>'
                if note else "")
        parts.append(f'''<div class="panel"><div class="cap">{html.escape(cap)}</div>
{draw(g, comp, PANEL_W, PANEL_H, evidence)}{flag}</div>''')
    parts.append('</div>')

    parts.append('''<div id="cite" hidden><div class="meta"></div><blockquote></blockquote>
<p class="hint" style="margin:8px 0 0">Passage as published by the Bank of Ghana. Press Escape to dismiss.</p></div>''')

    # -- the placement layer, shown apart from the graph -----------------------
    # Deliberately a table and not a diagram. Drawing it beside the components
    # would put it in the reader's eye as part of the same structure, which is
    # the exact confusion the layer exists to prevent.
    pl = metrics["placement_layer"]
    ifa = pl["if_admitted"]
    parts.append(f'''<h2>What was left out, and why</h2>
<p class="section-note">A separate finding, kept out of every number above.</p>
<p>The Commission&rsquo;s notice describes a second kind of relationship the Bank of
Ghana&rsquo;s does not: a fund manager placing client money in one of the 23, with
<em>no related-party claim attached</em>. Value moves. No insider relationship is
alleged. There are <strong>{pl["edges"]} such edges</strong>, from
<strong>{pl["fund_managers"]} fund managers</strong>, reaching
<strong>{pl["institutions_reached"]} of the 23</strong>.</p>
<p>Admitting them as ordinary edges would take the graph from
<strong>{ifa["components_related_party_only"]} components, largest
{ifa["largest_component_related_party_only"]}</strong>, to
<strong>{ifa["components_if_admitted"]} components, largest
{ifa["largest_component_if_admitted"]}</strong> &mdash; one structure holding most of
the graph. That structure is real. It is not an insider network: it is a set of
institutions that happen to share a fund manager who placed client money in both.
Presenting it as the headline would be the most flattering version of this project
and the least true one.</p>
<div class="scroll"><table>
<thead><tr><th>institution</th><th>fund managers placing client funds there</th></tr></thead>
<tbody>''')
    multi = pl["institutions_with_more_than_one_manager"]
    for name in sorted(multi):
        parts.append(f'<tr><td>{html.escape(name)}</td><td>'
                     f'{html.escape(", ".join(sorted(multi[name])))}</td></tr>')
    parts.append('</tbody></table></div>')
    unflagged = pl["institutions_unflagged_by_bog"]
    if unflagged:
        parts.append(
            '<p class="section-note">' + html.escape(", ".join(unflagged))
            + ' appears here, and is one of the six institutions the Bank of Ghana did '
              '<strong>not</strong> flag for related-party exposure. The 17-of-23 split '
              'is a property of that notice, not of the whole record.</p>')

    # -- typology: one series, so a single hue and no legend --------------------
    typ = {}
    for row in metrics["typology"]:
        typ[row["category"]] = typ.get(row["category"], 0) + row["edges"]
    top = max(typ.values())
    parts.append('''<h2>How value left the institutions</h2>
<p class="section-note">Every edge carries a relationship from a controlled vocabulary.
On this evidence base the mechanism counts carry more than any network measure does.</p>
<div class="bars">''')
    for cat, n in sorted(typ.items(), key=lambda kv: -kv[1]):
        parts.append(f'''<div class="bar-row"><span class="lab">{html.escape(cat)}</span>
<span class="bar-track"><span class="bar-fill" style="width:{100 * n / top:.1f}%"></span></span>
<span class="val">{n}</span></div>''')
    parts.append('</div>')

    # -- table view (the relief rule, and the accessible alternative) ----------
    parts.append('''<h2>Every edge, with its citation</h2>
<p class="section-note">The same data as the diagrams above, readable without colour.</p>
<details open><summary>Show the table</summary><div class="scroll"><table>
<thead><tr><th>id</th><th>from</th><th>to</th><th>relationship</th><th>amount</th>
<th>confidence</th><th>anchor</th></tr></thead><tbody>''')
    for u, v, key, d in sorted(g.edges(keys=True, data=True), key=lambda e: e[2]):
        amount = ""
        if d["amount_value"]:
            unit = "m" if d["amount_unit"] == "million" else ""
            amount = f"{d['amount_currency']} {d['amount_value']:,.2f}{unit}"
        anchor = evidence.get(key, {}).get("anchor", "")
        parts.append(
            f"<tr><td>{html.escape(key)}</td><td>{html.escape(g.nodes[u]['name'])}</td>"
            f"<td>{html.escape(g.nodes[v]['name'])}</td><td>{html.escape(d['relationship'])}</td>"
            f"<td class=\"num\">{html.escape(amount) or '&mdash;'}</td>"
            f"<td>{html.escape(d['confidence'])}</td>"
            f"<td class=\"num\">{html.escape(anchor.split(':')[-1] if anchor else '&mdash;')}</td></tr>")
    parts.append('</tbody></table></div></details>')

    parts.append(f'''<footer>
<p>Built from two documents: the Bank of Ghana&rsquo;s notice of 16 August 2019 revoking the
licences of 23 savings and loans companies and finance houses, and the Securities and Exchange
Commission&rsquo;s notice of 8 November 2019 revoking 53 fund-management licences. Every node
and edge carries a citation to a line in one of them; the quoted passages are in the
repository&rsquo;s evidence base. Inferred relationships are excluded from this page.</p>
<p><strong>What this cannot show is written down.</strong> No individual is named anywhere in
the evidence base, the graph is in {shape["components"]} pieces, and most relationships carry
no figure at all. The limitations are set out in full in
<a href="docs/LIMITATIONS.md">docs/LIMITATIONS.md</a>, and are worth reading before the
diagrams rather than after them.</p>
<p>Nothing here is an allegation. Each relationship restates what a regulator published, and
the page takes no position on any proceeding. Evidence base
<code>{metrics["verification"]["version"]}</code>, all
{sum(metrics["verification"]["counts"].values())} edges verified against source.</p>
</footer>
</div>
<script>{SCRIPT}</script>
</body></html>''')

    OUT.write_text("".join(parts), encoding="utf-8")
    con.close()
    print(f"components drawn : {len(components)} ({len(cases)} cases, {len(others)} panels)")
    print(f"edges with a quote: {sum(1 for v in evidence.values() if v['quote'])}")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.0f} KB)")


CASE_NOTES = [
    ("corp-unisecurities",
     {"title": "uniCredit Ghana, uniSecurities and the Hoda companies",
      "text": "The largest structure in the evidence base, and it takes both regulators "
              "to see it. The Bank of Ghana records that uniCredit, formerly Kantamanto "
              "Savings and Loans, was acquired by the Hoda Group of Companies in 2006, and "
              "that it was over-exposed to its sister company uniSecurities to the tune of "
              "GHS 160.10 million. The SEC then records uniSecurities placing client funds "
              "with seven related parties of its own, the first of which is Hoda Holdings. "
              "Whether Hoda Holdings and the Hoda Group are one entity is an open question "
              "in this repository, not an assumption: if they are, the ownership closes "
              "back on itself."}),
    ("corp-ideal-capital-partners",
     {"title": "Ideal Financial Holdings, Ideal Finance, FirsTrust and the group companies",
      "text": "A common owner above two separately licensed institutions that lent to each "
              "other. Ideal Financial Holdings acquired EZI Savings and Loans in 2014 and "
              "renamed it FirsTrust; Ideal Finance then carried related-party exposure to "
              "FirsTrust and to Ideal Capital Partners; in June 2019 the two applied to "
              "merge and the Bank of Ghana declined, both being insolvent. The SEC adds the "
              "piece the banking regulator had no reason to record: Ideal Capital Partners "
              "held related-party positions in the holding company, in FirsTrust, and in "
              "two non-financial group companies, Ideal Trade and Ideal Bottling. It is the "
              "only entity in the evidence base that connects two of the 23."}),
    ("corp-liberty-asset-management",
     {"title": "Midland and Liberty Asset Management",
      "text": "The smallest of the three and the most complete. The Bank of Ghana records "
              "Midland as over-exposed to related parties including Liberty Asset "
              "Management; the SEC records Liberty holding 9.45% of its funds with Midland, "
              "and 10.93% with Liberty Commodities. Each institution held the other, and "
              "value moves along both arrows. This is the only closed extraction loop in "
              "the evidence base, and neither regulator&rsquo;s notice shows it alone."}),
]



if __name__ == "__main__":
    build()
