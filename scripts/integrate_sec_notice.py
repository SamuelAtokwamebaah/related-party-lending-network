"""
Admit the SEC notice of 8 November 2019 as source S6, and record the GN appeal.

A one-off integration, run once and kept for the record. It refuses to run over
a later evidence base (see superseded_by below). Until v0.7 it claimed to be safe
to re-run, and it was not: it rewrote GN's status note to the v0.3 text.

Why this source matters. Phase 2 reported, from the Bank of Ghana notice alone,
that no entity connects two of the 23 institutions. That was true of that
document and is not true once this one is admitted. [Corrected at v0.7: the SEC
names FirsTrust, not Ideal Finance, among Ideal Capital Partners' related parties.
The connection needs both notices - the Bank of Ghana records Ideal Finance's
exposure to Ideal Capital Partners, and the SEC records Ideal Capital Partners
placing funds with FirsTrust.] The finding was always phrased as "the notice does not name one"
rather than "none exists", and this is why that distinction was worth keeping.

The GN status note is separate and is not evidence for any edge. On 21 May 2026
the Court of Appeal quashed the Bank of Ghana's revocation of GN Savings and
Loans' licence and the Bank has appealed to the Supreme Court. The repository's
standard is to take no position on live litigation and to keep contested
institutions out of worked examples, so GN keeps its cited edges but stops being
a case walkthrough, and every place it appears carries the status.

Usage:  python scripts/integrate_sec_notice.py
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

SEC = "sec-2019-11-08-fund-manager-revocation"
VERSION, TODAY = "v0.3", "2026-09-04"

SOURCES = [
    {"source_id": SEC,
     "title": ("Notice of revocation of licences of fund management companies and "
               "notification to the Registrar of Companies"),
     "publisher": "Securities and Exchange Commission, Ghana",
     "published_date": "2019-11-08", "doc_type": "regulator_notice",
     "url": ("https://sec.gov.gh/wp-content/uploads/Public-Notices/PUBLIC_NOTICE_OF_"
             "REVOCATION_OF_LICENCES_OF_FUND_MANAGEMENT_COMPANIES_AND_NOTIFICATION_"
             "TO_THE_REGISTRAR_OF_COMPANIES.pdf"),
     "local_path": f"sources/{SEC}.pdf", "retrieved_date": TODAY,
     "notes": ("Revokes 53 fund management licences under s.122(2)(b) of the Securities "
               "Industry Act, 2016 (Act 929). Text extracted with pypdf. Four "
               "counterparties already in this graph appear on it with their own "
               "regulatory record.")},
    {"source_id": "ca-2026-05-21-gn-savings-appeal",
     "title": "Court of Appeal decision restoring GN Savings and Loans' licence",
     "publisher": "Court of Appeal, Ghana", "published_date": "2026-05-21",
     "doc_type": "judgment",
     "url": ("https://ghana.dubawa.org/explainer-ghanas-court-of-appeal-overrules-"
             "revocation-of-gn-savings-and-loans-licence/"),
     "local_path": "", "retrieved_date": TODAY,
     "notes": ("RECORDED FROM PRESS REPORTING ON 4 SEPTEMBER 2026; THE JUDGMENT TEXT "
               "HAS NOT BEEN OBTAINED. Used only for the status note on GN Savings and "
               "Loans. It is not cited as evidence for any node or edge, and must not "
               "be until the judgment itself is read.")},
]

# (entity_id, canonical_name, entity_type, also_known_as)
ENTITIES = [
    ("corp-ideal-trade", "Ideal Trade Limited", "corporate_entity", ""),
    ("corp-ideal-bottling", "Ideal Bottling Limited", "corporate_entity", ""),
    ("corp-liberty-commodities", "Liberty Commodities Limited", "corporate_entity", ""),
    ("hold-hoda-holdings", "Hoda Holdings Ltd", "holding_company", ""),
    ("corp-intrepid-venture-capital", "Intrepid Venture Capital Ltd", "corporate_entity", ""),
    ("corp-premier-portfolio", "Premier Portfolio", "corporate_entity", ""),
    ("corp-integrated-properties", "Integrated Properties Ltd", "corporate_entity", ""),
    ("corp-bolton-portfolio", "Bolton Portfolio Ltd", "corporate_entity", ""),
    ("corp-numa-logistics", "Numa Logistics", "corporate_entity", ""),
    ("corp-alban-logistics", "Alban Logistics", "corporate_entity", ""),
]

# Quotes are pulled from the source by line range rather than retyped: the notice
# uses typographic apostrophes, and one retyped quote already failed the verbatim
# check for that reason. Each anchor starts at the section heading that names the
# firm, so the cited passage identifies whose related parties are listed - which
# is what rule 12 requires, and rightly so.
QUOTE_RANGES = {
    "L859": (859, 872),    # 14. Ideal Capital Partners
    "L945": (945, 956),    # 19. Liberty Asset Management
    "L1140": (1140, 1152),  # 30. Unisecurities (Ghana)
    "L658": (658, 674),    # 4. Blackshield, formerly Gold Coast Fund Management
}


def quote_from_source(first, last):
    text = (ROOT / "data" / "raw" / f"{SEC}.txt").read_text(encoding="utf-8")
    lines = text.split(chr(10))
    return re.sub(r"\s+", " ", " ".join(lines[first - 1:last])).strip()


# (edge_id, source, target, relationship, amount_note, anchor, review_note)
EDGES = [
    ("S001", "corp-ideal-capital-partners", "hold-ideal-financial-holdings",
     "placed_funds_with", "19% of assets under management across the four related parties named",
     f"{SEC}:L859", "SEC records Ideal Financial Holdings as a related party of Ideal Capital Partners"),
    ("S002", "corp-ideal-capital-partners", "inst-firstrust", "placed_funds_with",
     "19% of assets under management across the four related parties named", f"{SEC}:L859",
     "The link that connects one counterparty to two of the 23; source spells FirsTrust as Firstrust"),
    ("S003", "corp-ideal-capital-partners", "corp-ideal-trade", "placed_funds_with",
     "19% of assets under management across the four related parties named", f"{SEC}:L859",
     "Non-financial group company"),
    ("S004", "corp-ideal-capital-partners", "corp-ideal-bottling", "placed_funds_with",
     "19% of assets under management across the four related parties named", f"{SEC}:L859",
     "Non-financial group company"),
    ("S005", "corp-liberty-asset-management", "inst-midland", "placed_funds_with",
     "9.45% of funds under management; a ratio, not an amount", f"{SEC}:L945",
     "Midland was over-exposed to Liberty and Liberty held funds with Midland: each held the other"),
    ("S006", "corp-liberty-asset-management", "corp-liberty-commodities", "placed_funds_with",
     "10.93% of funds under management; a ratio, not an amount", f"{SEC}:L945", ""),
    ("S007", "corp-unisecurities", "hold-hoda-holdings", "placed_funds_with", "",
     f"{SEC}:L1140",
     "Whether Hoda Holdings Ltd is the Hoda Group of Companies that acquired uniCredit is undecided; see RR004"),
    ("S008", "corp-unisecurities", "corp-intrepid-venture-capital", "placed_funds_with", "", f"{SEC}:L1140", ""),
    ("S009", "corp-unisecurities", "corp-premier-portfolio", "placed_funds_with", "", f"{SEC}:L1140", ""),
    ("S010", "corp-unisecurities", "corp-integrated-properties", "placed_funds_with", "", f"{SEC}:L1140", ""),
    ("S011", "corp-unisecurities", "corp-bolton-portfolio", "placed_funds_with", "", f"{SEC}:L1140", ""),
    ("S012", "corp-unisecurities", "corp-numa-logistics", "placed_funds_with", "", f"{SEC}:L1140", ""),
    ("S013", "corp-unisecurities", "corp-alban-logistics", "placed_funds_with", "", f"{SEC}:L1140", ""),
    ("S014", "corp-gold-coast-fund-management", "corp-ghana-growth-fund", "placed_funds_with",
     "99.41% of funds under management; a ratio, not an amount", f"{SEC}:L658",
     "Both are named in the BoG notice as sister companies of GN; this documents the link between them"),
]

RESOLUTION = [
    ("RR004", "Hoda Holdings Ltd", "hold-hoda-holdings", "Hoda Group of Companies",
     "hold-hoda-group", "0.55",
     "SEC names Hoda Holdings Ltd as a related party of uniSecurities; the BoG notice says "
     "the Hoda Group of Companies acquired uniCredit. Same group or two entities?",
     "If the same, one entity connects uniCredit and uniSecurities on the record"),
    ("RR005", "Intermarket Asset Management Limited (formerly CDH Asset Management Limited)",
     "", "CDH Savings and Loans Ltd.", "inst-cdh", "0.30",
     "Entry 15 on the SEC list shares the CDH name with institution 6. Shared naming only.",
     "No edge created. A shared name is not evidence of a relationship"),
    ("RR006", "Legacy Fund Management Limited (formerly Legacy Financial Services Limited)",
     "", "Legacy Capital Savings and Loans Ltd.", "inst-legacy-capital", "0.30",
     "Entry 18 on the SEC list shares the Legacy name with institution 19. Shared naming only.",
     "No edge created. A shared name is not evidence of a relationship"),
]

GN_STATUS = (
    "On 21 May 2026 the Court of Appeal quashed the Bank of Ghana's "
    "16 August 2019 revocation of this institution's licence and ordered it restored; "
    "the Bank of Ghana has appealed to the Supreme Court and the matter is pending. "
    "The edges below remain as published by the Bank of Ghana and are attributed to it. "
    "Recorded from press reporting on 4 September 2026; the judgment has not been read."
)

CHANGES = [
    ("C005", "add", "source", SEC,
     "Admitted the SEC notice of 8 November 2019 as a second primary source. Four "
     "counterparties already in the graph appear on it with their own regulatory record."),
    ("C006", "add", "batch", "sec-edges",
     "Fourteen edges from the SEC notice, including Ideal Capital Partners' related-party "
     "positions in both Ideal Finance and FirsTrust. This is the first entity in the "
     "evidence base to connect two of the 23 institutions, and it falsifies the Phase 2 "
     "finding that none does - a finding that was, correctly, stated as a property of the "
     "Bank of Ghana notice rather than of the world."),
    ("C007", "correct", "entity", "inst-gn",
     "Added a status note recording the Court of Appeal decision of 21 May 2026 quashing "
     "the revocation, and the pending Supreme Court appeal. GN's edges are unchanged and "
     "remain attributed to the Bank of Ghana, but the institution is no longer presented "
     "as a worked example, per the standard that contested institutions are excluded from "
     "case studies."),
    ("C008", "correct", "entity", "corp-ghana-growth-fund",
     "Alias for Gold Coast Advisors Limited reclassified from [variant] to [later]: the "
     "SEC notice states Ghana Growth Fund Limited is 'now Gold Coast Advisors Limited'."),
]


def append(name, rows, key):
    """Append rows whose key is not already present. Never rewrites an existing row."""
    path = DATA / name
    existing = list(csv.DictReader(path.open(encoding="utf-8")))
    fields = list(existing[0].keys())
    seen = {r[key] for r in existing}
    added = [r for r in rows if r[key] not in seen]
    for r in added:
        for f in fields:
            r.setdefault(f, "")
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(existing + [{f: r.get(f, "") for f in fields} for r in added])
    print(f"  {name:26} +{len(added)}")
    return len(added)


def superseded_by():
    """The latest version in the changelog, if it is later than this script's.

    These scripts were each run once and are kept as the record of how a source
    entered the evidence base. Re-running one over a later evidence base would
    write back text that a later version corrected, so they refuse.
    """
    with (DATA / "changelog.csv").open(encoding="utf-8", newline="") as fh:
        versions = {r["version"] for r in csv.DictReader(fh)}
    key = lambda v: tuple(int(x) for x in v.lstrip("v").split("."))
    later = sorted((v for v in versions if key(v) > key(VERSION)), key=key)
    return later[-1] if later else None


def main():
    later = superseded_by()
    if later:
        print(f"The evidence base is already at {later}. This script integrated {VERSION} "
              "and is kept as a record; re-running it would restore text that later "
              "versions corrected. Nothing written.")
        return 0
    append("sources.csv", SOURCES, "source_id")

    append("evidence.csv",
           [{"anchor": f"{SEC}:{ref}", "source_id": SEC,
             "quote": quote_from_source(*span), "page": "", "extracted_date": TODAY}
            for ref, span in QUOTE_RANGES.items()], "anchor")

    append("entities.csv",
           [{"entity_id": eid, "canonical_name": name, "entity_type": etype,
             "also_known_as": aka, "scope_class": "counterparty", "regulator": "none",
             "jurisdiction": "GH", "member_count": "", "is_named": "1",
             "admitted_by_edge_id": "", "evidence_anchors": "", "notes": "Named in the SEC notice"}
            for eid, name, etype, aka in ENTITIES], "entity_id")

    append("edges.csv",
           [{"edge_id": eid, "source_entity_id": src, "target_entity_id": tgt,
             "relationship": rel, "amount_value": "", "amount_currency": "",
             "amount_unit": "", "amount_basis": "", "amount_note": note,
             "as_at_date": "", "confidence": "documented", "evidence_anchors": anchor,
             "review_note": review, "version_added": VERSION, "version_removed": ""}
            for eid, src, tgt, rel, note, anchor, review in EDGES], "edge_id")

    append("resolution_review.csv",
           [{"candidate_id": cid, "name_a": a, "entity_id_a": ida, "name_b": b,
             "entity_id_b": idb, "similarity": sim, "reason": reason,
             "decision": "undecided", "decided_date": "", "decision_note": note}
            for cid, a, ida, b, idb, sim, reason, note in RESOLUTION], "candidate_id")

    append("changelog.csv",
           [{"change_id": cid, "version": VERSION, "change_date": TODAY,
             "change_type": ctype, "object_type": otype, "object_id": oid,
             "reason": reason, "source_id": SEC if otype != "entity" else ""}
            for cid, ctype, otype, oid, reason in CHANGES], "change_id")

    # In-place corrections to existing rows.
    path = DATA / "entities.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    fields = list(rows[0].keys())
    if "status_note" not in fields:
        fields.append("status_note")
    for r in rows:
        r.setdefault("status_note", "")
        if r["entity_id"] == "inst-gn":
            r["status_note"] = GN_STATUS
        if r["entity_id"] == "corp-ghana-growth-fund":
            r["also_known_as"] = "Gold Coast Advisors Limited[later]"
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows({f: r.get(f, "") for f in fields} for r in rows)
    print("  entities.csv               status_note on inst-gn; alias corrected on Ghana Growth Fund")

    # New edges are from a new source and have not been checked by hand.
    path = DATA / "verification.csv"
    ver = list(csv.DictReader(path.open(encoding="utf-8")))
    have = {r["edge_id"] for r in ver}
    for eid, *_ in EDGES:
        if eid not in have:
            ver.append({"edge_id": eid, "decision": "pending", "note": "",
                        "verified_date": "", "verified_by": ""})
    ver.sort(key=lambda r: r["edge_id"])
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, lineterminator="\n", fieldnames=["edge_id", "decision", "note",
                                           "verified_date", "verified_by"])
        w.writeheader()
        w.writerows(ver)
    print(f"  verification.csv           {sum(1 for r in ver if r['decision']=='pending')} pending")


if __name__ == "__main__":
    main()
