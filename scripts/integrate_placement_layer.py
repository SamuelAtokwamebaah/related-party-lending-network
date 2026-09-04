"""
v0.4 - the rest of the SEC notice, and the placement layer.

v0.3 admitted four sections of the SEC notice: the four fund managers that were
already counterparties in the graph. That was the wrong stopping point. The
notice has 53 sections, and a scan of all of them finds eleven that name one of
the 23 institutions. Eight were unread.

Three of those eight state a related-party relationship in the Commission's own
words, and they belong in the related-party graph:

    Standard Securities (formerly ASN Investments) -> ASN Financial Services
    Legacy Fund Management                         -> Legacy Capital Savings
    Nordea Capital                                 -> Commerz Savings and Loans

The other six describe a fund manager placing client money in one of the 23 with
no related-party claim attached. Value moves; no insider relationship is alleged.
Admitting those as ordinary edges would connect most of the seventeen components
through shared fund managers and would make the graph claim something the
documents do not say. They go in as a separate layer instead, marked
'placement' in relationship_types, filtered out of v_institution_profile, and
excluded by default from every related-party figure.

The script is idempotent: it appends only rows whose key is absent, so a second
run changes nothing. Quotes are extracted from the source by line range rather
than retyped, because retyping one cost a rejected build at v0.3 - a straight
apostrophe where the source uses a typographic one.

Usage:  python scripts/integrate_placement_layer.py
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
VERSION = "v0.4"
TODAY = "2026-09-04"

SEC = "sec-2019-11-08-fund-manager-revocation"
BOG = "bog-2019-08-16-savings-loans-revocation"


def read_source(source_id):
    """Lines numbered as grep, sed and an editor number them - form feeds are
    page furniture inside a line, never a line break."""
    path = DATA / "raw" / f"{source_id}.txt"
    text = path.read_text(encoding="utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def quote(source_id, first, last):
    lines = read_source(source_id)
    body = " ".join(lines[first - 1:last])
    return " ".join(body.split())


def load(name):
    with (DATA / name).open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader), reader.fieldnames


def save(name, rows, fields):
    with (DATA / name).open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def append(name, key, new_rows):
    """Append only rows whose key is not already present. Returns how many."""
    rows, fields = load(name)
    seen = {r[key] for r in rows}
    added = 0
    for row in new_rows:
        if row[key] in seen:
            continue
        rows.append({f: row.get(f, "") for f in fields})
        seen.add(row[key])
        added += 1
    if added:
        save(name, rows, fields)
    return added


# ---------------------------------------------------------------------------
# 1. Evidence: the eleven passages, anchored at their section headings.
#
# Anchoring at the heading is what v0.3 learned the hard way. The Commission
# names a firm in its heading and then calls it "the firm", so a passage
# anchored at the bullet names the counterparty but never says whose it is.
# ---------------------------------------------------------------------------

EVIDENCE = [
    # (anchor_line, last_line, source)
    (508, 523, SEC),    # 17. Standard Securities (formerly ASN Investments)
    (722, 737, SEC),    # 7.  Corporate Hills
    (835, 851, SEC),    # 13. Goldstreet
    (875, 884, SEC),    # 15. Integrity
    (919, 932, SEC),    # 18. Legacy Fund Management
    (964, 972, SEC),    # 20. Monarch
    (974, 991, SEC),    # 21. Mutual Integrity
    (1014, 1026, SEC),  # 23. Nordea
    (1054, 1063, SEC),  # 25. Procap
    # Section headings in the Bank of Ghana notice. These exist so rule 12 can
    # be extended to institutions without disturbing an anchor already verified
    # by hand: the verified anchor stays exactly as it is and the heading is
    # added beside it.
    (713, 713, BOG),    # 15. GLOBAL ACCESS
    (861, 861, BOG),    # 17. IDEAL FINANCE
    (1040, 1040, BOG),  # 20. MIDLAND
    (1100, 1100, BOG),  # 22. UNICREDIT
]

# Edges whose institution endpoint is not named in the passage they cite. The
# heading anchor is appended, never substituted.
HEADING_ANCHORS = {
    "E020": f"{BOG}:L713",
    "E024": f"{BOG}:L861",
    "E025": f"{BOG}:L861",
    "E028": f"{BOG}:L1040",
    "E029": f"{BOG}:L1040",
    "E030": f"{BOG}:L1040",
    "E032": f"{BOG}:L1100",
}

# Names the notices use that the canonical name does not cover. Only two are
# needed; the rest of the Commission's spellings already match on the
# distinctive head of the canonical name.
NEW_ALIASES = {
    "inst-firstrust": "First Trust Savings & Loans[variant]",
    "inst-legacy-capital": "Legacy Savings & Loans[variant]",
}

# ---------------------------------------------------------------------------
# 2. The nine fund managers.
# ---------------------------------------------------------------------------

FUND_MANAGERS = [
    ("fm-standard-securities", "Standard Securities Limited",
     "ASN Investments Limited[former]"),
    ("fm-legacy-fund-management", "Legacy Fund Management Limited",
     "Legacy Financial Services Ltd[former]"),
    ("fm-nordea-capital", "Nordea Capital Limited", ""),
    ("fm-corporate-hills", "Corporate Hills Investment Limited", ""),
    ("fm-goldstreet", "Goldstreet Fund Management Limited",
     "Goldstreet Investments Ltd[former]"),
    ("fm-integrity", "Integrity Fund Management Ltd", ""),
    ("fm-monarch-capital", "Monarch Capital Limited", ""),
    ("fm-mutual-integrity", "Mutual Integrity Asset Management Limited",
     "Mutual Integrity Limited[variant]"),
    ("fm-procap", "Procap Finance Limited", ""),
]

# ---------------------------------------------------------------------------
# 3. Edges.
#
# amount_value is recorded only where the source states a figure for that one
# counterparty. Where it states one share across several - "over 80% ... in
# revoked savings & loans including, Midland, First Trust and Legacy" - the
# basis is combined_total and the note carries the wording, so the figure can
# never be read as belonging to a single institution. That is the same mistake
# that put a projected merger injection into FirsTrust's extraction total once.
# ---------------------------------------------------------------------------

COMBINED_80 = ("Stated as 'Over 80% placement of client funds in revoked savings & "
               "loans' across Midland, FirsTrust and Legacy Capital together. The "
               "notice gives no per-institution split, and the figure is a floor.")
COMBINED_54 = ("Stated as '54% of placement of client funds with Commerz Savings & "
               "Loans, CDH Savings & Loans' together. The notice gives no "
               "per-institution split.")
COMBINED_68 = ("Stated as 'Over 68% placement in revoked Savings and Loans "
               "institutions including Midland Savings and Loans and FirsTrust' "
               "together. The notice gives no per-institution split, the figure is "
               "a floor, and 'including' leaves the list open.")

EDGES = [
    # --- related-party layer: the Commission's own words -------------------
    ("P001", "fm-standard-securities", "inst-asn", "placed_funds_with",
     "", "", "", "", "",
     f"{SEC}:L508",
     "The notice says 'Related party placement with related party called ASN "
     "Financial Services Limited'. No figure is stated for it."),
    ("P002", "fm-legacy-fund-management", "inst-legacy-capital", "placed_funds_with",
     "18", "", "percent", "ratio_only", "",
     f"{SEC}:L919",
     "'Placement of 18% of funds in related party Legacy Capital Savings "
     "Limited'. Settles resolution candidate RR006: the Commission states the "
     "relationship, so it no longer rests on a shared name."),
    ("P003", "fm-nordea-capital", "inst-commerz", "placed_funds_with",
     "50", "", "percent", "ratio_only", "",
     f"{SEC}:L1014",
     "'Placement of 50% of Funds under management with a related party; Commerz "
     "Savings and Loans'. Commerz is one of the six institutions the Bank of "
     "Ghana did not flag for related-party exposure. The direction is into "
     "Commerz, so this does not show Commerz's own insiders extracting from it."),

    # --- placement layer: no related-party claim in the source -------------
    ("P004", "fm-corporate-hills", "inst-asn", "placed_client_funds_with",
     "54.19", "", "percent", "ratio_only", "",
     f"{SEC}:L722", ""),
    ("P005", "fm-goldstreet", "inst-ideal-finance", "placed_client_funds_with",
     "50.61", "", "percent", "ratio_only", "",
     f"{SEC}:L835", ""),
    ("P006", "fm-goldstreet", "inst-firstrust", "placed_client_funds_with",
     "10.06", "", "percent", "ratio_only", "",
     f"{SEC}:L835", ""),
    ("P007", "fm-integrity", "inst-midland", "placed_client_funds_with",
     "80", "", "percent", "combined_total", COMBINED_80,
     f"{SEC}:L875", ""),
    ("P008", "fm-integrity", "inst-firstrust", "placed_client_funds_with",
     "80", "", "percent", "combined_total", COMBINED_80,
     f"{SEC}:L875", ""),
    ("P009", "fm-integrity", "inst-legacy-capital", "placed_client_funds_with",
     "80", "", "percent", "combined_total", COMBINED_80,
     f"{SEC}:L875", ""),
    ("P010", "fm-monarch-capital", "inst-legacy-capital", "placed_client_funds_with",
     "78", "", "percent", "ratio_only", "",
     f"{SEC}:L964", ""),
    ("P011", "fm-mutual-integrity", "inst-commerz", "placed_client_funds_with",
     "54", "", "percent", "combined_total", COMBINED_54,
     f"{SEC}:L974",
     "The second document to put Commerz on the receiving end of a placement, "
     "and the second reason the six unflagged institutions are unflagged only "
     "in the Bank of Ghana notice."),
    ("P012", "fm-mutual-integrity", "inst-cdh", "placed_client_funds_with",
     "54", "", "percent", "combined_total", COMBINED_54,
     f"{SEC}:L974", ""),
    ("P013", "fm-procap", "inst-midland", "placed_client_funds_with",
     "68", "", "percent", "combined_total", COMBINED_68,
     f"{SEC}:L1054", ""),
    ("P014", "fm-procap", "inst-firstrust", "placed_client_funds_with",
     "68", "", "percent", "combined_total", COMBINED_68,
     f"{SEC}:L1054", ""),
    ("P015", "fm-standard-securities", "inst-express", "placed_client_funds_with",
     "", "", "", "", "",
     f"{SEC}:L508",
     "Listed under 'Other Placements', distinct from the related-party "
     "placement in the same bullet. No figure is stated."),
    ("P016", "fm-standard-securities", "inst-midland", "placed_client_funds_with",
     "", "", "", "", "",
     f"{SEC}:L508",
     "Listed under 'Other Placements', distinct from the related-party "
     "placement in the same bullet. No figure is stated."),
]

EDGE_FIELDS = ("edge_id", "source_entity_id", "target_entity_id", "relationship",
               "amount_value", "amount_currency", "amount_unit", "amount_basis",
               "amount_note", "evidence_anchors", "review_note")

# Percentages the Commission states for edges already in the base at v0.3. They
# were dropped because the schema could not hold a ratio.
BACKFILL = {
    "S005": ("9.45", "percent", "ratio_only", ""),
    "S006": ("10.93", "percent", "ratio_only", ""),
    "S014": ("99.41", "percent", "ratio_only", ""),
    "S001": ("19", "percent", "combined_total",
             "Stated as '19% of AUM in related parties' across Ideal Financial "
             "Holdings, FirsTrust, Ideal Trade and Ideal Bottling together. No "
             "per-counterparty split is given."),
    "S002": ("19", "percent", "combined_total",
             "Stated as '19% of AUM in related parties' across Ideal Financial "
             "Holdings, FirsTrust, Ideal Trade and Ideal Bottling together. No "
             "per-counterparty split is given."),
    "S003": ("19", "percent", "combined_total",
             "Stated as '19% of AUM in related parties' across Ideal Financial "
             "Holdings, FirsTrust, Ideal Trade and Ideal Bottling together. No "
             "per-counterparty split is given."),
    "S004": ("19", "percent", "combined_total",
             "Stated as '19% of AUM in related parties' across Ideal Financial "
             "Holdings, FirsTrust, Ideal Trade and Ideal Bottling together. No "
             "per-counterparty split is given."),
}

CHANGELOG = [
    ("C009", "add", "batch", "placement-layer-entities",
     "Nine fund managers from the SEC notice of 8 November 2019, whose sections "
     "name one of the 23 institutions and were not read at v0.3. A scan of all "
     "53 sections found eleven naming one of the 23; four were already in the "
     "base, and these are the other eight plus Standard Securities, which names "
     "three.", SEC),
    ("C010", "add", "batch", "related-party-edges-p001-p003",
     "Three edges the Commission states in related-party terms: Standard "
     "Securities (formerly ASN Investments) with ASN Financial Services, Legacy "
     "Fund Management with Legacy Capital Savings, and Nordea Capital with "
     "Commerz Savings and Loans. The third is the notable one: Commerz is among "
     "the six institutions the Bank of Ghana did not flag for related-party "
     "exposure, so the clean 17/6 split is a property of that notice and not of "
     "the record as a whole.", SEC),
    ("C011", "add", "batch", "placement-edges-p004-p016",
     "Thirteen edges recording fund managers placing client funds in the 23 "
     "with no related-party claim in the source. They enter a separate layer, "
     "are filtered out of v_institution_profile, and are excluded by default "
     "from the related-party figures. Admitting them as ordinary edges would "
     "connect most of the seventeen components through shared fund managers and "
     "would present a due-diligence failure as an insider relationship.", SEC),
    ("C012", "correct", "schema", "relationship_types.layer",
     "relationship_types gains a layer column, and edges may now carry a "
     "percentage: amount_unit accepts 'percent', which takes no currency and "
     "must pair with basis ratio_only or combined_total. The Commission states "
     "its figures as shares of a fund's own book, and at v0.3 every one of them "
     "was dropped because the schema could not hold a ratio.", SEC),
    ("C013", "correct", "batch", "sec-edge-amounts",
     "Percentages backfilled onto seven edges added at v0.3: 9.45% Liberty with "
     "Midland, 10.93% Liberty with Liberty Commodities, 99.41% Blackshield with "
     "Ghana Growth Fund, and 19% of Ideal's AUM across four related parties, "
     "recorded as a combined total on each of the four so it cannot be read as "
     "belonging to one.", SEC),
    ("C014", "correct", "rule", "load.py-rule-12",
     "Rule 12 extended to institution endpoints, which were exempt by omission "
     "rather than by decision. Seven documented edges failed it: their passages "
     "name the counterparty but not the institution. Each gains a second anchor "
     "at its section heading in the notice; the anchor already verified by hand "
     "is unchanged, so the verification pass still stands.", BOG),
    ("C015", "correct", "resolution", "RR006",
     "Decided. The Commission does not merely share the Legacy name across two "
     "firms: it states that Legacy Capital Savings Limited is a related party of "
     "Legacy Fund Management Limited. The relationship is documented and is "
     "recorded as edge P002. The two remain distinct entities.", SEC),
]


def main():
    print(f"integrating the placement layer at {VERSION}\n")

    # --- evidence ---------------------------------------------------------
    ev_rows = []
    for first, last, source_id in EVIDENCE:
        ev_rows.append({
            "anchor": f"{source_id}:L{first}",
            "source_id": source_id,
            "quote": quote(source_id, first, last),
            "page": "",
            "extracted_date": TODAY,
        })
    print(f"  evidence            + {append('evidence.csv', 'anchor', ev_rows)}")

    # --- entities ---------------------------------------------------------
    ent_rows = []
    for eid, name, aka in FUND_MANAGERS:
        ent_rows.append({
            "entity_id": eid, "canonical_name": name,
            "entity_type": "corporate_entity", "also_known_as": aka,
            "scope_class": "counterparty", "regulator": "SEC", "jurisdiction": "GH",
            "member_count": "", "is_named": "1", "admitted_by_edge_id": "",
            "evidence_anchors": "", "notes":
                "Licence revoked by the Securities and Exchange Commission on "
                "8 November 2019 under s.122(2)(b) of Act 929.",
            "status_note": "",
        })
    print(f"  entities            + {append('entities.csv', 'entity_id', ent_rows)}")

    # --- aliases onto existing entities -----------------------------------
    rows, fields = load("entities.csv")
    touched = 0
    for row in rows:
        alias = NEW_ALIASES.get(row["entity_id"])
        if not alias:
            continue
        have = [a.strip() for a in (row["also_known_as"] or "").split(";") if a.strip()]
        if alias in have:
            continue
        row["also_known_as"] = "; ".join(have + [alias])
        touched += 1
    if touched:
        save("entities.csv", rows, fields)
    print(f"  aliases             + {touched}")

    # --- edges ------------------------------------------------------------
    edge_rows = []
    for values in EDGES:
        row = dict(zip(EDGE_FIELDS, values))
        row["as_at_date"] = ""
        row["confidence"] = "documented"
        row["version_added"] = VERSION
        row["version_removed"] = ""
        edge_rows.append(row)
    print(f"  edges               + {append('edges.csv', 'edge_id', edge_rows)}")

    # --- backfilled amounts and heading anchors ---------------------------
    rows, fields = load("edges.csv")
    amounts, anchors = 0, 0
    for row in rows:
        fill = BACKFILL.get(row["edge_id"])
        if fill and not row["amount_value"]:
            row["amount_value"], row["amount_unit"], row["amount_basis"] = fill[:3]
            row["amount_currency"] = ""
            if fill[3]:
                row["amount_note"] = fill[3]
            amounts += 1
        extra = HEADING_ANCHORS.get(row["edge_id"])
        if extra:
            have = [a.strip() for a in row["evidence_anchors"].split(";") if a.strip()]
            if extra not in have:
                row["evidence_anchors"] = "; ".join(have + [extra])
                anchors += 1
    if amounts or anchors:
        save("edges.csv", rows, fields)
    print(f"  amounts backfilled  ~ {amounts}")
    print(f"  heading anchors     ~ {anchors}")

    # --- resolution decision ----------------------------------------------
    rows, fields = load("resolution_review.csv")
    decided = 0
    for row in rows:
        if row["candidate_id"] == "RR006" and row["decision"] == "undecided":
            # The question this table asks is same-or-different. That two
            # entities are related is a separate fact and lives in edges.
            row["decision"] = "different"
            row["decided_date"] = TODAY
            row["decision_note"] = (
                "Different entities. The shared name is not what settles it: the SEC "
                "notice states 'Placement of 18% of funds in related party Legacy "
                "Capital Savings Limited', so the Commission describes a relationship "
                "between two firms rather than one firm under two names. Recorded as "
                "edge P002.")
            decided += 1
    if decided:
        save("resolution_review.csv", rows, fields)
    print(f"  resolutions decided ~ {decided}")

    # --- changelog --------------------------------------------------------
    cl_rows = [{
        "change_id": cid, "version": VERSION, "change_date": TODAY,
        "change_type": ctype, "object_type": otype, "object_id": oid,
        "reason": reason, "source_id": src,
    } for cid, ctype, otype, oid, reason, src in CHANGELOG]
    print(f"  changelog           + {append('changelog.csv', 'change_id', cl_rows)}")

    # --- verification: new edges are pending, and say so ------------------
    v_rows = [{"edge_id": v[0], "decision": "", "note": "",
               "verified_date": "", "verified_by": ""} for v in EDGES]
    print(f"  verification rows   + {append('verification.csv', 'edge_id', v_rows)}")

    print("\nnow run: python scripts/load.py")


if __name__ == "__main__":
    sys.exit(main())
