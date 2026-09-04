"""
Build the verification pack: one review sheet per institution.

The seeded evidence base is a first pass. This turns it into something you can
check section by section against the notice, without flipping between four files.

For each of the 23 institutions the sheet shows:

  1. every edge seeded against it, with the quote and the anchor behind it
  2. every passage in that section of the notice, marked cited or not

Part 2 is the one that matters. An edge you can see is easy to check; an edge
that should exist and does not is invisible unless the passages are laid out
beside what was extracted from them. The uncited passages are where the misses
are, and the extractor has already been wrong twice in exactly that way.

Record decisions in data/verification.csv, which this script creates and then
only ever adds to - it never overwrites a decision you have already made.

Usage:  python scripts/build_review_pack.py
"""

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from phase0_extract_evidence import (ANY_SIGNAL, blocks, read_lines,  # noqa: E402
                                     split_sections, tidy)

DATA = ROOT / "data"
OUT = ROOT / "docs" / "review"
VERIFICATION = DATA / "verification.csv"
SOURCE_ID = "bog-2019-08-16-savings-loans-revocation"

VERIFICATION_FIELDS = [
    "edge_id", "decision", "note", "verified_date", "verified_by",
]


def load(name):
    with (DATA / name).open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def slug(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return re.sub(r"-(limited|ltd|company|co)$", "", s)[:48]


def match_section_to_entity(section_name, entities):
    """Match an ALL-CAPS section heading to an entity_id."""
    def norm(text):
        text = re.sub(r"\(.*?\)", " ", text.lower())
        text = re.sub(r"[^a-z ]", " ", text)
        drop = {"limited", "ltd", "company", "co", "the", "savings", "and",
                "loans", "loan", "finance", "financial", "services", "house", "ghana"}
        return tuple(w for w in text.split() if w not in drop)

    want = norm(section_name)
    for row in entities:
        if row["scope_class"] != "core_23":
            continue
        if norm(row["canonical_name"]) == want:
            return row
    # Fall back to overlap, which covers the spelling drift between the notice's
    # headings and the canonical names.
    best, best_score = None, 0
    for row in entities:
        if row["scope_class"] != "core_23":
            continue
        got = set(norm(row["canonical_name"]))
        score = len(got & set(want))
        if score > best_score:
            best, best_score = row, score
    return best if best_score else None


def amount_str(edge):
    if not edge.get("amount_value"):
        return "—"
    unit = "m" if edge.get("amount_unit") == "million" else ""
    basis = edge.get("amount_basis") or "?"
    return f"{edge.get('amount_currency','?')} {edge['amount_value']}{unit} ({basis})"


def main():
    lines = read_lines()
    sections = split_sections(lines)
    entities = load("entities.csv")
    edges = load("edges.csv")
    evidence = {r["anchor"]: r["quote"] for r in load("evidence.csv")}
    by_id = {r["entity_id"]: r for r in entities}

    cited_anchors = set()
    for e in edges:
        for a in (e.get("evidence_anchors") or "").split(";"):
            if a.strip():
                cited_anchors.add(a.strip())

    edges_by_entity = {}
    for e in edges:
        for field in ("source_entity_id", "target_entity_id"):
            edges_by_entity.setdefault(e[field], []).append(e)

    existing = {}
    if VERIFICATION.exists():
        existing = {r["edge_id"]: r for r in load("verification.csv")}

    OUT.mkdir(parents=True, exist_ok=True)
    index, total_uncited, total_flagged, unmatched_sections = [], 0, 0, []

    for number, name, start, end in sections:
        entity = match_section_to_entity(name, entities)
        if entity is None:
            unmatched_sections.append(name)
            continue
        eid = entity["entity_id"]

        seen, mine = set(), []
        for e in edges_by_entity.get(eid, []):
            if e["edge_id"] not in seen:
                seen.add(e["edge_id"])
                mine.append(e)
        mine.sort(key=lambda e: e["edge_id"])

        passages = [(n, tidy(b)) for n, b in blocks(lines, start, end)]
        passages = [(n, t) for n, t in passages if len(t) >= 40]
        uncited = [(n, t) for n, t in passages
                   if f"{SOURCE_ID}:L{n}" not in cited_anchors]
        # Split by whether the passage carries relationship vocabulary. The
        # flagged ones are where a missed edge is likely; the rest are mostly
        # capital-adequacy boilerplate and are listed compactly so the section
        # can still be scanned in full without burying the candidates.
        flagged = [(n, t) for n, t in uncited if ANY_SIGNAL.search(t)]
        rest = [(n, t) for n, t in uncited if not ANY_SIGNAL.search(t)]
        total_uncited += len(uncited)
        total_flagged += len(flagged)

        md = [
            f"# {number}. {entity['canonical_name']}",
            "",
            f"`{eid}` · notice section **L{start}–L{end}** · "
            f"{len(mine)} seeded edge(s) · {len(uncited)} uncited passage(s)",
            "",
            "Read the section in `data/raw/` from L{0} to L{1}, then work through both "
            "parts below. Record every decision in `data/verification.csv`.".format(start, end),
            "",
            "---",
            "",
            "## Part 1 — edges seeded against this institution",
            "",
            "For each: does the quote support the relationship, the direction, the "
            "amount and its basis, and the confidence class?",
            "",
        ]
        if not mine:
            md += ["_No edge was seeded for this institution._", ""]

        for e in mine:
            other = ("target", e["target_entity_id"]) if e["source_entity_id"] == eid \
                else ("source", e["source_entity_id"])
            counterparty = by_id.get(other[1], {}).get("canonical_name", other[1])
            direction = "→" if other[0] == "target" else "←"
            prior = existing.get(e["edge_id"], {}).get("decision", "")
            md += [
                f"### {e['edge_id']} — {entity['canonical_name']} {direction} {counterparty}",
                "",
                f"| | |",
                f"|---|---|",
                f"| relationship | `{e['relationship']}` |",
                f"| amount | {amount_str(e)} |",
                f"| confidence | `{e['confidence']}` |",
                f"| anchor | `{e.get('evidence_anchors') or '(none — inferred)'}` |",
                f"| current decision | {prior or '**pending**'} |",
                "",
            ]
            for a in (e.get("evidence_anchors") or "").split(";"):
                a = a.strip()
                if a and a in evidence:
                    md += [f"> {evidence[a]}", ""]
            if e.get("review_note"):
                md += [f"*Note carried from compilation:* {e['review_note']}", ""]
            if e.get("amount_note"):
                md += [f"*Amount note:* {e['amount_note']}", ""]

        md += [
            "---",
            "",
            "## Part 2a — uncited passages that mention a relationship",
            "",
            "These carry related-party, affiliate, ownership, officer or exposure "
            "wording and no edge cites them. This is where a missed relationship is "
            "most likely. For each: does it describe a relationship between this "
            "institution and another party? If so it needs an edge, and the passage "
            "needs a row in `data/evidence.csv` under the anchor shown.",
            "",
        ]
        if not flagged:
            md += ["_None. Every passage carrying relationship wording is cited._", ""]
        for n, body in flagged:
            excerpt = body if len(body) <= 420 else body[:420] + " …"
            md += [f"- **`{SOURCE_ID}:L{n}`**", f"  > {excerpt}", ""]

        md += [
            "---",
            "",
            f"## Part 2b — the rest of the section ({len(rest)} passages)",
            "",
            "Mostly capital adequacy, net worth and reporting breaches. Listed so the "
            "section can be scanned in full — the extractor's vocabulary has been wrong "
            "twice already, so its judgement about what is irrelevant is not final.",
            "",
        ]
        if not rest:
            md += ["_None._", ""]
        for n, body in rest:
            excerpt = body if len(body) <= 150 else body[:150] + " …"
            md += [f"- `L{n}` {excerpt}"]
        md += [""]

        path = OUT / f"{number:02d}-{slug(entity['canonical_name'])}.md"
        path.write_text("\n".join(md) + "\n", encoding="utf-8")
        index.append((number, entity["canonical_name"], path.name, len(mine),
                      len(flagged), len(rest)))

    # verification.csv: create it, or add rows for edges that are not in it yet.
    # Never touch a decision already recorded.
    rows = [existing[e["edge_id"]] for e in edges if e["edge_id"] in existing]
    added = 0
    for e in edges:
        if e["edge_id"] not in existing:
            rows.append({"edge_id": e["edge_id"], "decision": "pending",
                         "note": "", "verified_date": "", "verified_by": ""})
            added += 1
    rows.sort(key=lambda r: r["edge_id"])
    with VERIFICATION.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=VERIFICATION_FIELDS)
        w.writeheader()
        w.writerows(rows)

    idx = [
        "# Verification pack",
        "",
        "One sheet per institution. Each pairs the edges seeded against it with the "
        "passages they came from, and lists every passage in that section that no edge "
        "cites.",
        "",
        "The seeded rows are a first pass built by script from the Phase 0 candidate "
        "sheet. Nothing here should be treated as verified until it carries a decision "
        "in `data/verification.csv`.",
        "",
        "Decisions: `confirmed`, `corrected`, `rejected`, `pending`.",
        "",
        "Work the sheets with a non-zero **To check** count first: those sections "
        "contain a passage carrying relationship wording that no edge cites.",
        "",
        "| # | Institution | Sheet | Edges | To check | Rest |",
        "|---|---|---|---|---|---|",
    ]
    for number, name, filename, n_edges, n_flagged, n_rest in index:
        mark = f"**{n_flagged}**" if n_flagged else "0"
        idx.append(f"| {number} | {name} | [{filename}]({filename}) | {n_edges} | {mark} | {n_rest} |")
    idx += [
        "",
        f"**Totals:** {sum(i[3] for i in index)} seeded edges to verify, "
        f"{total_flagged} uncited passages carrying relationship wording, "
        f"{total_uncited - total_flagged} other passages, across {len(index)} institutions.",
        "",
        "Regenerate with `python scripts/build_review_pack.py`. It rewrites the sheets "
        "and adds rows to `data/verification.csv` for any new edge, but never overwrites "
        "a decision already recorded there.",
        "",
        "## The other notice",
        "",
        "These sheets cover the Bank of Ghana notice only. The Securities and Exchange "
        "Commission's notice is arranged by fund manager rather than by institution, so "
        "its pack is built separately and lives in [sec/](sec/):",
        "",
        "- [sec/01-sections-with-edges.md](sec/01-sections-with-edges.md) — every section "
        "an edge cites, reproduced in full, with the edges drawn from it",
        "- [sec/02-coverage.md](sec/02-coverage.md) — all 53 sections, marked for whether "
        "they name one of the 23 and whether an edge exists. Read this one first: v0.3 "
        "read four sections and stopped, and eight more named one of the 23.",
        "",
        "Regenerate with `python scripts/build_sec_review.py`.",
    ]
    (OUT / "README.md").write_text("\n".join(idx) + "\n", encoding="utf-8")

    print(f"sheets written        : {len(index)}")
    print(f"seeded edges covered  : {sum(i[3] for i in index)}")
    print(f"uncited, to check     : {total_flagged}")
    print(f"uncited, rest         : {total_uncited - total_flagged}")
    print(f"verification.csv      : {len(rows)} rows ({added} added, "
          f"{len(rows) - added} decisions preserved)")
    if unmatched_sections:
        print(f"UNMATCHED SECTIONS    : {unmatched_sections}")
    print(f"\nstart at docs/review/README.md")


if __name__ == "__main__":
    main()
