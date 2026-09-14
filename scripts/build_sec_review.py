"""
Build the verification pack for the SEC notice.

build_review_pack.py covers the Bank of Ghana notice, one sheet per institution.
This is the same idea for the other regulator, and it is organised the other way
round: the Commission's notice is arranged by fund manager, so a sheet is a fund
manager and the institutions appear inside it.

Two sheets, not one per section:

  01-sections-with-edges.md   the 13 sections an edge cites, each shown in full,
                              with the edges drawn from it
  02-coverage.md              all 53 sections, marked for whether they name one
                              of the 23 and whether an edge exists

The second sheet is the one that matters, and it exists because of what went
wrong here. v0.3 read four sections - the four fund managers already in the
graph - and stopped. Nine more named one of the 23 and were missed. A pack that
only shows the sections already cited would have hidden that, exactly as a pack
showing only cited passages would have hidden a missed relationship in the Bank
of Ghana notice. So every section is listed, and the ones with no edge are
listed most plainly of all.

Usage:  python scripts/build_sec_review.py
"""

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "docs" / "review" / "sec"
SOURCE_ID = "sec-2019-11-08-fund-manager-revocation"

# A section heading in this notice: "14. IDEAL CAPITAL PARTNERS LIMITED".
# Only past the contents list at the top, which uses the same shape.
HEADING = re.compile(r"^\s*(\d{1,2})\.\s+([A-Z][A-Z0-9 ,.&()'-]{6,})\s*$")
BODY_STARTS = 190


def load(name):
    with (DATA / name).open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def read_lines():
    text = (DATA / "raw" / f"{SOURCE_ID}.txt").read_text(encoding="utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def sections(lines):
    found = []
    for i, line in enumerate(lines, 1):
        m = HEADING.match(line)
        if m and i > BODY_STARTS:
            found.append([int(m.group(1)), m.group(2).strip(), i, None])
    for n, row in enumerate(found):
        row[3] = found[n + 1][2] - 1 if n + 1 < len(found) else len(lines)
    return [tuple(r) for r in found]


def letters_only(text, drop_parens=False):
    """Strip to letters, dropping 'and' and '&'.

    The two notices write the same institution as "Midland Savings and Loans
    Company Limited", "Midland Savings & Loans" and, thanks to the PDF's
    spacing, "Midland S avings & Loans". Flattening to letters and dropping the
    connector makes all three the same string, which is the only way to compare
    them without an alias for every typographic accident.
    """
    # Parentheses are dropped from a *name* - "(formerly Gold Coast Fund
    # Management Limited)" is not part of the canonical name - but never from a
    # passage. The Commission lists Ideal's related parties inside brackets, so
    # stripping them from the body hid FirsTrust in the section that names it.
    text = text.lower()
    if drop_parens:
        text = re.sub(r"\(.*?\)", " ", text)
    text = re.sub(r"\band\b|&", " ", text)
    return re.sub(r"[^a-z]", "", text)


# How much of a flattened name must appear. Twelve letters is enough to separate
# "Alpha Capital Savings and Loans" from "Alpha Cap Securities" and "First Ghana
# Savings and Loans" from "first quarter", both of which a looser match reported
# as hits. It is short enough to still catch "Ideal Finance Ltd" for "Ideal
# Finance Limited".
KEY_LETTERS = 12


def institution_patterns(entities):
    """Flattened name prefixes for the 23, canonical names and aliases alike."""
    pats = {}
    for row in entities:
        if row["scope_class"] != "core_23":
            continue
        names = [row["canonical_name"]]
        for raw in (row.get("also_known_as") or "").split(";"):
            raw = raw.strip()
            if raw:
                names.append(re.sub(r"\[\w+\]$", "", raw).strip())
        keys = {letters_only(n, drop_parens=True)[:KEY_LETTERS] for n in names}
        pats[row["canonical_name"]] = sorted(k for k in keys if len(k) >= KEY_LETTERS)
    return pats


def squash(text):
    return re.sub(r"\s+", " ", text).strip().lower()


def amount_str(edge):
    if not edge.get("amount_value"):
        return "—"
    if edge.get("amount_unit") == "percent":
        return f"{edge['amount_value']}% ({edge.get('amount_basis') or '?'})"
    unit = "m" if edge.get("amount_unit") == "million" else ""
    return (f"{edge.get('amount_currency', '?')} {edge['amount_value']}{unit} "
            f"({edge.get('amount_basis') or '?'})")


def main():
    lines = read_lines()
    secs = sections(lines)
    entities = load("entities.csv")
    by_id = {r["entity_id"]: r for r in entities}
    edges = load("edges.csv")
    rels = {r["relationship"]: r for r in load("relationship_types.csv")}
    evidence = {r["anchor"]: r["quote"] for r in load("evidence.csv")}
    decisions = {r["edge_id"]: r["decision"] for r in load("verification.csv")}
    pats = institution_patterns(entities)

    # Which section does each anchor fall in?
    def section_of(line_no):
        """Returns the section's start line, not its number.

        The notice numbers its sections 1-21 and then starts again at 1, so a
        number is not a key: two different fund managers are both "17", and
        keying on the number filed Standard Securities' edges under Kripa
        Capital and Goldstreet's under Mcottley.
        """
        for num, name, start, end in secs:
            if start <= line_no <= end:
                return start
        return None

    edges_by_section = {}
    for e in edges:
        for anchor in (e.get("evidence_anchors") or "").split(";"):
            anchor = anchor.strip()
            if not anchor.startswith(SOURCE_ID + ":L"):
                continue
            at = section_of(int(anchor.rsplit(":L", 1)[1]))
            if at is not None:
                edges_by_section.setdefault(at, []).append((e, anchor))

    OUT.mkdir(parents=True, exist_ok=True)

    # --- sheet 1: the sections an edge cites, in full ---------------------
    md = [
        "# SEC notice — sections with edges",
        "",
        f"`{SOURCE_ID}` · {len(secs)} sections in the notice · "
        f"{len(edges_by_section)} carry an edge",
        "",
        "Each section below is reproduced in full from `data/raw/`, followed by the "
        "edges drawn from it. For each edge: does the passage support the "
        "relationship, its direction, the amount and its basis, the layer, and the "
        "confidence class? Record decisions in `data/verification.csv`.",
        "",
        "**On the layer.** A `related_party` edge is one the Commission describes in "
        "related-party terms. A `placement` edge is a fund manager placing client "
        "money in one of the 23 with no such claim in the source. If a passage marked "
        "`placement` does state a related-party relationship, that is a finding: the "
        "edge is in the wrong layer and belongs in the headline figures.",
        "",
        "---",
        "",
    ]
    for num, name, start, end in secs:
        if start not in edges_by_section:
            continue
        md += [
            f"## §{num}. {name}",
            "",
            f"notice **L{start}–L{end}**",
            "",
            "```",
        ]
        md += [line.rstrip() for line in lines[start - 1:end] if line.strip()]
        md += ["```", ""]
        for edge, anchor in sorted(edges_by_section[start],
                                   key=lambda x: x[0]["edge_id"]):
            src = by_id.get(edge["source_entity_id"], {}).get(
                "canonical_name", edge["source_entity_id"])
            tgt = by_id.get(edge["target_entity_id"], {}).get(
                "canonical_name", edge["target_entity_id"])
            rel = rels.get(edge["relationship"], {})
            md += [
                f"### {edge['edge_id']} — {src} → {tgt}",
                "",
                "| | |",
                "|---|---|",
                f"| relationship | `{edge['relationship']}` |",
                f"| layer | `{rel.get('layer', '?')}` |",
                f"| moves value | {'yes' if rel.get('extracts_value') == '1' else 'no'} |",
                f"| amount | {amount_str(edge)} |",
                f"| confidence | `{edge['confidence']}` |",
                f"| anchor | `{anchor}` |",
                f"| current decision | {decisions.get(edge['edge_id']) or '**pending**'} |",
                "",
            ]
            if edge.get("amount_note"):
                md += [f"*Amount note:* {edge['amount_note']}", ""]
            if edge.get("review_note"):
                md += [f"*Note carried from compilation:* {edge['review_note']}", ""]
        md += ["---", ""]

    (OUT / "01-sections-with-edges.md").write_text("\n".join(md) + "\n", encoding="utf-8",
                                                   newline="\n")

    # --- sheet 2: coverage of all 53 sections -----------------------------
    rows, missed = [], 0
    for num, name, start, end in secs:
        body = letters_only(" ".join(lines[start - 1:end]))
        named = sorted(inst for inst, keys in pats.items()
                       if any(k in body for k in keys))
        n_edges = len(edges_by_section.get(start, []))
        if named and not n_edges:
            missed += 1
        rows.append((num, name, start, end, named, n_edges))

    md = [
        "# SEC notice — coverage of all sections",
        "",
        f"`{SOURCE_ID}` · {len(secs)} sections · "
        f"{sum(1 for r in rows if r[4])} name one of the 23 · "
        f"{sum(1 for r in rows if r[5])} carry an edge",
        "",
        "This sheet exists because of a real miss. v0.3 read four sections — the four "
        "fund managers already in the graph — and stopped there. Two of those four name "
        "one of the 23; nine more sections did, and were not read. Listing every section "
        "is what makes that kind "
        "of gap visible instead of invisible.",
        "",
        "The **names one of the 23** column is produced by string matching against "
        "canonical names and aliases. It is a prompt to look, not a finding: it will "
        "miss a spelling nobody has recorded as an alias yet, and it will flag a "
        "coincidence of names. Both have happened.",
        "",
    ]
    if missed:
        md += [
            f"> **{missed} section(s) name one of the 23 and carry no edge.** Each is "
            "marked below. Either the passage does not state a relationship, or an "
            "edge is missing.",
            "",
        ]
    else:
        md += ["> Every section that names one of the 23 carries at least one edge.", ""]
    md += [
        "| § | fund manager | lines | names one of the 23 | edges |",
        "|---|---|---|---|---|",
    ]
    for num, name, start, end, named, n_edges in rows:
        flag = " **←**" if named and not n_edges else ""
        md.append(f"| {num} | {name.title()} | L{start}–L{end} | "
                  f"{', '.join(named) if named else '—'} | {n_edges or '—'}{flag} |")
    md += [
        "",
        "Sections naming none of the 23 are still part of the notice and may name a "
        "counterparty already in the graph under another name. That is the residual "
        "risk this sheet does not cover.",
        "",
    ]
    (OUT / "02-coverage.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")

    print(f"  sections            {len(secs)}")
    print(f"  with an edge        {len(edges_by_section)}")
    print(f"  name one of the 23  {sum(1 for r in rows if r[4])}")
    print(f"  named but no edge   {missed}")
    print(f"wrote {OUT.relative_to(ROOT)}/01-sections-with-edges.md and 02-coverage.md")


if __name__ == "__main__":
    sys.exit(main())
