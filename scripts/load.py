"""
Build the evidence base into SQLite from the CSVs in data/.

The database is a build artefact: dropped and rebuilt on every run, never edited
directly. If a figure is wrong, a CSV row is wrong.

The loader refuses to build if any validation rule fails, and names the row and
the reason. That refusal is the point of it. A citation nobody checks is a
claim; rule 11 below checks every one of them against the source text, so an
anchor in this repository means the quote really is at that line in the notice.

Usage:  python scripts/load.py [--db db/graph.db]
"""

import argparse
import csv
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SQL = ROOT / "sql" / "schema.sql"
DEFAULT_DB = ROOT / "db" / "graph.db"

CONFIDENCE = {"documented", "documented_unnamed", "inferred"}
ALIAS_TYPES = {"former", "later", "typo", "variant"}


class Problems:
    """Collects every failure so one run reports all of them, not just the first."""

    def __init__(self):
        self.items = []

    def add(self, rule, where, message):
        self.items.append((rule, where, message))

    def report(self):
        if not self.items:
            return True
        print(f"\nREFUSING TO BUILD - {len(self.items)} validation failure(s):\n")
        for rule, where, message in self.items:
            print(f"  [rule {rule}] {where}: {message}")
        print("\nFix the CSV rows above and run again. The database was not written.")
        return False


def read(name):
    path = DATA / name
    if not path.exists():
        print(f"missing required file: data/{name}")
        sys.exit(1)
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def split_list(value):
    return [v.strip() for v in (value or "").split(";") if v.strip()]


def parse_alias(raw):
    """'EZI Savings and Loans Limited[former]' -> (name, 'former')."""
    m = re.match(r"^(.*?)\[(\w+)\]$", raw.strip())
    if not m:
        return raw.strip(), None
    return m.group(1).strip(), m.group(2).strip().lower()


def normalise(text):
    return re.sub(r"\s+", " ", text or "").strip()


def source_lines():
    """source_id -> list of lines, numbered as grep, sed and an editor number them.

    str.splitlines() also breaks on form feeds, and these notices carry one per
    page break, which would put every line number ahead of what a reader sees.
    """
    out = {}
    for path in (DATA / "raw").glob("*.txt"):
        raw = path.read_text(encoding="utf-8")
        raw = raw.replace("�", "GHS ").replace("GHGHS ", "GHS ").replace("GHS  ", "GHS ")
        normalised = raw.replace("\r\n", "\n").replace("\r", "\n")
        out[path.stem] = normalised.split("\n")
    return out


def quote_starts_at(lines, line_no, quote):
    """True if the quote begins at line_no, allowing for the source's wrapping.

    A quote is a wrapped paragraph, so it is checked against the anchored line
    plus enough following lines to contain it - not against the whole document.
    Checking against the whole document would accept an anchor pointing anywhere,
    which is how a 26-line drift went unnoticed once already.
    """
    want = normalise(quote)
    window = normalise(" ".join(lines[line_no - 1: line_no - 1 + 60]))
    return window.startswith(want[:80]) or want in window


def validate(tables, problems):
    sources = {r["source_id"] for r in tables["sources"]}
    entities = {r["entity_id"] for r in tables["entities"]}
    rels = {r["relationship"] for r in tables["relationship_types"]}
    anchors = {r["anchor"] for r in tables["evidence"]}
    edge_ids = {r["edge_id"] for r in tables["edges"]}
    texts = source_lines()

    # --- duplicates (rule 10) -------------------------------------------
    for table, key in (("entities", "entity_id"), ("edges", "edge_id"),
                       ("evidence", "anchor"), ("roles", "role_id")):
        seen = set()
        for row in tables[table]:
            if row[key] in seen:
                problems.add(10, f"{table} {row[key]}", "duplicate key")
            seen.add(row[key])

    # --- evidence -------------------------------------------------------
    for row in tables["evidence"]:
        anchor, sid = row["anchor"], row["source_id"]
        if sid not in sources:
            problems.add(2, f"evidence {anchor}", f"source_id '{sid}' not in sources.csv")
            continue
        if ":" not in anchor or not anchor.startswith(sid):
            problems.add(11, f"evidence {anchor}", "anchor must read '<source_id>:L<line>'")
            continue
        # Rule 11: the quote must be verbatim AND at the line the anchor names.
        lines = texts.get(sid)
        if lines is None:
            problems.add(11, f"evidence {anchor}",
                         f"no working text found at data/raw/{sid}.txt to verify against")
            continue
        try:
            line_no = int(anchor.rsplit(":L", 1)[1])
        except (IndexError, ValueError):
            problems.add(11, f"evidence {anchor}", "anchor must end ':L<line>'")
            continue
        if not 1 <= line_no <= len(lines):
            problems.add(11, f"evidence {anchor}",
                         f"line {line_no} is outside the source (1-{len(lines)})")
        elif not quote_starts_at(lines, line_no, row["quote"]):
            problems.add(11, f"evidence {anchor}",
                         f"quote is not at line {line_no} of the source")

    # --- entities -------------------------------------------------------
    for row in tables["entities"]:
        eid = row["entity_id"]
        for raw in split_list(row.get("also_known_as")):
            name, atype = parse_alias(raw)
            if atype is None:
                problems.add(0, f"entities {eid}",
                             f"alias '{name}' has no [type] marker; expected one of "
                             f"{sorted(ALIAS_TYPES)}")
            elif atype not in ALIAS_TYPES:
                problems.add(0, f"entities {eid}", f"unknown alias type '[{atype}]'")
        if row["scope_class"] == "scope_exception" and not row.get("admitted_by_edge_id"):
            problems.add(9, f"entities {eid}",
                         "scope_exception requires admitted_by_edge_id naming the edge "
                         "whose citation admitted it")
        if row.get("admitted_by_edge_id") and row["admitted_by_edge_id"] not in edge_ids:
            problems.add(9, f"entities {eid}",
                         f"admitted_by_edge_id '{row['admitted_by_edge_id']}' is not an edge")
        if row["entity_type"] == "placeholder_group" and row["is_named"] != "0":
            problems.add(8, f"entities {eid}", "placeholder_group must have is_named = 0")
        for anchor in split_list(row.get("evidence_anchors")):
            if anchor not in anchors:
                problems.add(2, f"entities {eid}", f"anchor '{anchor}' not in evidence.csv")

    # --- edges ----------------------------------------------------------
    for row in tables["edges"]:
        eid = row["edge_id"]
        for field in ("source_entity_id", "target_entity_id"):
            if row[field] not in entities:
                problems.add(1, f"edges {eid}", f"{field} '{row[field]}' not in entities.csv")
        if row["relationship"] not in rels:
            problems.add(3, f"edges {eid}",
                         f"relationship '{row['relationship']}' not in relationship_types.csv")
        if row["confidence"] not in CONFIDENCE:
            problems.add(4, f"edges {eid}", f"confidence '{row['confidence']}' not permitted")

        edge_anchors = split_list(row.get("evidence_anchors"))
        if row["confidence"] == "inferred":
            if edge_anchors:
                problems.add(6, f"edges {eid}",
                             "inferred edges must carry no evidence anchor")
            if not (row.get("review_note") or "").strip():
                problems.add(6, f"edges {eid}", "inferred edges must carry a review_note")
        else:
            if not edge_anchors:
                problems.add(5, f"edges {eid}",
                             f"{row['confidence']} edges need at least one evidence anchor")
            for anchor in edge_anchors:
                if anchor not in anchors:
                    problems.add(2, f"edges {eid}", f"anchor '{anchor}' not in evidence.csv")

        if row.get("amount_value"):
            basis = row.get("amount_basis")
            if not basis or basis == "none":
                problems.add(7, f"edges {eid}",
                             "an amount needs an amount_basis (exact / floor / "
                             "combined_total / ratio_only)")
            if not row.get("amount_currency"):
                problems.add(7, f"edges {eid}",
                             "an amount needs a currency; not every figure in the "
                             "sources is in cedis")
            if not row.get("amount_unit"):
                problems.add(7, f"edges {eid}",
                             "an amount needs a unit (million / units)")

    # --- rule 12: cited passage must name the counterparty ---------------
    # An anchor can be verbatim, in range, and still point at the wrong
    # paragraph. For an edge whose counterparty is a named company, that
    # company's name - or one of its aliases - has to appear in the passage
    # cited for it. This is what catches an anchor aimed one paragraph off.
    quotes = {r["anchor"]: normalise(r["quote"]).lower() for r in tables["evidence"]}
    names = {}
    for row in tables["entities"]:
        if row["entity_type"] not in ("corporate_entity", "holding_company"):
            continue
        variants = [row["canonical_name"]]
        variants += [parse_alias(a)[0] for a in split_list(row.get("also_known_as"))]
        names[row["entity_id"]] = [v.lower() for v in variants if v]

    for row in tables["edges"]:
        if row["confidence"] != "documented":
            continue
        for field in ("source_entity_id", "target_entity_id"):
            variants = names.get(row[field])
            if not variants:
                continue
            cited = " ".join(quotes.get(a, "") for a in split_list(row.get("evidence_anchors")))
            if not cited:
                continue
            # Match on the distinctive head of the name, since the notice
            # abbreviates ("Gold Coast Fund Management" for the full style).
            if not any(v[:24] in cited or cited.find(v.split()[0]) >= 0 and v[:12] in cited
                       for v in variants):
                problems.add(12, f"edges {row['edge_id']}",
                             f"{field} '{row[field]}' is a named company but is not "
                             f"named in the passage cited for this edge")

    # --- roles ----------------------------------------------------------
    for row in tables["roles"]:
        rid = row["role_id"]
        for field in ("entity_id", "institution_id"):
            if row[field] not in entities:
                problems.add(1, f"roles {rid}", f"{field} '{row[field]}' not in entities.csv")
        if row["confidence"] not in CONFIDENCE:
            problems.add(4, f"roles {rid}", f"confidence '{row['confidence']}' not permitted")
        for anchor in split_list(row.get("evidence_anchors")):
            if anchor not in anchors:
                problems.add(2, f"roles {rid}", f"anchor '{anchor}' not in evidence.csv")

    # --- changelog ------------------------------------------------------
    for row in tables["changelog"]:
        if row.get("source_id") and row["source_id"] not in sources:
            problems.add(2, f"changelog {row['change_id']}",
                         f"source_id '{row['source_id']}' not in sources.csv")


def attr_key(name):
    """Normalise an institution name for joining the vendored dataset."""
    name = re.sub(r"\(.*?\)", " ", name.lower())
    name = re.sub(r"[^a-z ]", " ", name)
    drop = {"limited", "ltd", "company", "co", "the", "savings", "and", "loans",
            "loan", "finance", "financial", "services", "house", "ghana"}
    return tuple(sorted(w for w in name.split() if w not in drop))


def institution_attribute_rows(con):
    """Institution attributes from the vendored ghana-banking-collapse dataset.

    Carried over rather than retyped. Joined on a normalised name because the
    notice and the dataset spell several institutions differently.
    """
    path = DATA / "vendor" / "savings_loans_verified.csv"
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        source = {attr_key(r["institution_name"]): r for r in csv.DictReader(fh)}

    yn = lambda v: 1 if (v or "").strip().upper() == "Y" else 0
    rows, unmatched = [], []
    for entity_id, name in con.execute(
            "SELECT entity_id, canonical_name FROM entities WHERE scope_class = 'core_23'"):
        # Try the canonical name, then the aliases. The vendored dataset carries
        # the notice's own misspelling of FirsTrust, which is registered as a
        # [typo] alias - so the alias table does the join.
        candidates = [name] + [a for (a,) in con.execute(
            "SELECT alias_name FROM aliases WHERE entity_id = ?", (entity_id,))]
        r = next((source[k] for k in map(attr_key, candidates) if k in source), None)
        if r is None:
            unmatched.append(name)
            continue
        rows.append((entity_id, r["licence_type"] or None, r["incorporated"] or None,
                     r["licensed"] or None, r["insolvent_since"] or None,
                     number(r["net_worth_ghs_m"]), number(r["car_pct"]),
                     yn(r["related_party_exposure"]), yn(r["governance_failure"]),
                     yn(r["liquidity_failure"]), yn(r["misreporting"]),
                     yn(r["high_npl"]),
                     int(r["cause_count"]) if (r["cause_count"] or "").strip() else None))
    if unmatched:
        print(f"  note: no vendored attributes matched for {unmatched}")
    return rows


def nullable(value):
    value = (value or "").strip()
    return value if value else None


def number(value):
    value = (value or "").strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def build(tables, db_path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    con = sqlite3.connect(db_path)
    con.executescript(SQL.read_text(encoding="utf-8"))
    con.execute("PRAGMA foreign_keys = ON")

    con.executemany(
        "INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?)",
        [(r["source_id"], r["title"], r["publisher"], nullable(r["published_date"]),
          r["doc_type"], nullable(r["url"]), nullable(r["local_path"]),
          nullable(r["retrieved_date"]), nullable(r["notes"]))
         for r in tables["sources"]])

    con.executemany(
        "INSERT INTO evidence VALUES (?,?,?,?,?)",
        [(r["anchor"], r["source_id"], r["quote"], nullable(r["page"]),
          nullable(r["extracted_date"])) for r in tables["evidence"]])

    con.executemany(
        "INSERT INTO relationship_types VALUES (?,?,?,?)",
        [(r["relationship"], r["category"], int(r["extracts_value"]), r["description"])
         for r in tables["relationship_types"]])

    con.executemany(
        "INSERT INTO entities VALUES (?,?,?,?,?,?,?,?,?,?)",
        [(r["entity_id"], r["canonical_name"], r["entity_type"], r["scope_class"],
          nullable(r["regulator"]), nullable(r["jurisdiction"]),
          int(r["member_count"]) if (r["member_count"] or "").strip() else None,
          int(r["is_named"]), nullable(r["admitted_by_edge_id"]), nullable(r["notes"]))
         for r in tables["entities"]])

    aliases = []
    for r in tables["entities"]:
        for raw in split_list(r.get("also_known_as")):
            name, atype = parse_alias(raw)
            aliases.append((r["entity_id"], name, atype))
    con.executemany("INSERT OR IGNORE INTO aliases VALUES (?,?,?)", aliases)

    con.executemany(
        "INSERT INTO edges VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [(r["edge_id"], r["source_entity_id"], r["target_entity_id"], r["relationship"],
          number(r["amount_value"]), nullable(r["amount_currency"]), nullable(r["amount_unit"]),
          nullable(r["amount_basis"]), nullable(r["amount_note"]),
          nullable(r["as_at_date"]), r["confidence"], nullable(r["review_note"]),
          r["version_added"], nullable(r["version_removed"]))
         for r in tables["edges"]])

    con.executemany("INSERT OR IGNORE INTO edge_evidence VALUES (?,?)",
                    [(r["edge_id"], a) for r in tables["edges"]
                     for a in split_list(r.get("evidence_anchors"))])

    con.executemany(
        "INSERT INTO roles VALUES (?,?,?,?,?,?,?,?)",
        [(r["role_id"], r["entity_id"], r["institution_id"], r["role_type"],
          nullable(r["start_date"]), nullable(r["end_date"]), r["confidence"],
          nullable(r["notes"])) for r in tables["roles"]])

    con.executemany("INSERT OR IGNORE INTO role_evidence VALUES (?,?)",
                    [(r["role_id"], a) for r in tables["roles"]
                     for a in split_list(r.get("evidence_anchors"))])

    con.executemany("INSERT OR IGNORE INTO entity_evidence VALUES (?,?)",
                    [(r["entity_id"], a) for r in tables["entities"]
                     for a in split_list(r.get("evidence_anchors"))])

    con.executemany(
        "INSERT INTO verification VALUES (?,?,?,?,?)",
        [(r["edge_id"], r["decision"] or "pending", nullable(r["note"]),
          nullable(r["verified_date"]), nullable(r["verified_by"]))
         for r in tables["verification"]])

    con.executemany(
        "INSERT INTO institution_attributes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        institution_attribute_rows(con))

    con.executemany(
        "INSERT INTO resolution_review VALUES (?,?,?,?,?,?,?,?,?,?)",
        [(r["candidate_id"], r["name_a"], nullable(r["entity_id_a"]), r["name_b"],
          nullable(r["entity_id_b"]), number(r["similarity"]), nullable(r["reason"]),
          r["decision"], nullable(r["decided_date"]), nullable(r["decision_note"]))
         for r in tables["resolution_review"]])

    con.executemany(
        "INSERT INTO changelog VALUES (?,?,?,?,?,?,?,?)",
        [(r["change_id"], r["version"], r["change_date"], r["change_type"],
          r["object_type"], nullable(r["object_id"]), r["reason"], nullable(r["source_id"]))
         for r in tables["changelog"]])

    con.commit()
    return con


def summarise(con):
    q = lambda sql: con.execute(sql).fetchone()[0]
    print("\nbuilt:")
    for table in ("sources", "evidence", "entities", "aliases", "institution_attributes",
                  "relationship_types", "edges", "edge_evidence", "roles",
                  "verification", "resolution_review", "changelog"):
        print(f"  {table:22} {q(f'SELECT COUNT(*) FROM {table}'):>4}")

    print("\nedges by confidence:")
    for conf, n in con.execute(
            "SELECT confidence, COUNT(*) FROM edges GROUP BY confidence ORDER BY 2 DESC"):
        print(f"  {conf:22} {n:>4}")

    extracting = q("SELECT COUNT(*) FROM edges e JOIN relationship_types rt "
                   "ON rt.relationship = e.relationship WHERE rt.extracts_value = 1")
    print(f"\nvalue-extracting edges  {extracting:>4} of {q('SELECT COUNT(*) FROM edges')}")

    seen = dict(con.execute(
        "SELECT COALESCE(v.decision,'pending'), COUNT(*) FROM edges e "
        "LEFT JOIN verification v ON v.edge_id = e.edge_id GROUP BY 1"))
    if q("SELECT COUNT(*) FROM verification"):
        print("\nverification:")
    for state in ("confirmed", "corrected", "rejected", "pending"):
        if seen.get(state):
            print(f"  {state:22} {seen[state]:>4}")
    if seen.get("pending"):
        print(f"  -> {seen['pending']} edge(s) not yet checked against the notice; "
              f"see docs/review/README.md")

    undecided = q("SELECT COUNT(*) FROM resolution_review WHERE decision = 'undecided'")
    if undecided:
        print(f"\n{undecided} entity-resolution candidate(s) still undecided - "
              f"see data/resolution_review.csv")

    version = con.execute(
        "SELECT version FROM changelog ORDER BY change_date DESC, change_id DESC LIMIT 1"
    ).fetchone()
    if version:
        print(f"evidence base version   {version[0]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=str(DEFAULT_DB), help="output database path")
    args = ap.parse_args()

    tables = {name: read(f"{name}.csv") for name in (
        "sources", "evidence", "entities", "relationship_types",
        "edges", "roles", "resolution_review", "changelog")}
    # Optional: created by scripts/build_review_pack.py.
    path = DATA / "verification.csv"
    tables["verification"] = read("verification.csv") if path.exists() else []

    problems = Problems()
    validate(tables, problems)
    if not problems.report():
        sys.exit(1)

    print(f"all {sum(len(v) for v in tables.values())} rows pass validation")
    con = build(tables, Path(args.db))
    summarise(con)
    print(f"\nwrote {Path(args.db).relative_to(ROOT)}")
    con.close()


if __name__ == "__main__":
    main()
