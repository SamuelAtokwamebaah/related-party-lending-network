"""
Phase 1 - seed the CSV templates from the Phase 0 candidate sheet.

Reshapes docs/phase0/candidate-edges.csv into the six-file model agreed at the
Phase 1 review, and pulls each quoted passage verbatim out of the source text by
its line anchor rather than retyping it.

This is a one-off migration, not the validating loader. It produces a starting
point for hand verification: every row it writes is a first pass, and the
compilation work of reading the notice and extending these files is done by hand.

Run once:  python scripts/phase1_seed_from_phase0.py
Outputs the six templates plus relationship_types.csv into data/.
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from phase0_extract_evidence import blocks, read_lines, tidy  # noqa: E402

CANDIDATES = ROOT / "docs" / "phase0" / "candidate-edges.csv"
DATA = ROOT / "data"
SOURCE_ID = "bog-2019-08-16-savings-loans-revocation"
VERSION = "v0.1"
TODAY = "2026-09-04"

# --------------------------------------------------------------------------
# Entities. entity_id is stable and never reused: it is what edges, roles and
# every later finding point at, so a renamed institution keeps its id and gains
# an alias rather than getting a new one.
# --------------------------------------------------------------------------

# (entity_id, canonical_name, also_known_as, scope_class, regulator, jurisdiction)
INSTITUTIONS = [
    ("inst-accent", "Accent Financial Services Limited", "", "core_23", "BoG", "GH"),
    ("inst-adom", "Adom Savings and Loans Limited", "", "core_23", "BoG", "GH"),
    ("inst-alltime", "AllTime Finance Limited", "Alltime[variant]", "core_23", "BoG", "GH"),
    ("inst-alpha-capital", "Alpha Capital Savings and Loans Ltd.", "", "core_23", "BoG", "GH"),
    ("inst-asn", "ASN Financial Services Limited", "", "core_23", "BoG", "GH"),
    ("inst-cdh", "CDH Savings and Loans Ltd.", "CDH Savings & Loans Limited[variant]", "core_23", "BoG", "GH"),
    ("inst-commerz", "Commerz Savings and Loans Limited",
     "Sterling Savings and Loans Limited[former]", "core_23", "BoG", "GH"),
    ("inst-crest", "Crest Finance House Limited",
     "Apex Finance House Limited[former]", "core_23", "BoG", "GH"),
    ("inst-dream", "Dream Finance Limited", "", "core_23", "BoG", "GH"),
    ("inst-express", "Express Savings and Loan Limited", "", "core_23", "BoG", "GH"),
    ("inst-first-allied", "First Allied Savings and Loans Limited",
     "FASL[variant]", "core_23", "BoG", "GH"),
    ("inst-first-african", "First African Savings and Loans Limited",
     "First African Savings & Loans Company Limited[variant]", "core_23", "BoG", "GH"),
    ("inst-first-ghana", "First Ghana Savings and Loans Limited", "", "core_23", "BoG", "GH"),
    ("inst-firstrust", "FirsTrust Savings and Loans Limited",
     "EZI Savings and Loans Limited[former];FirstTrust[typo];FTSL[variant]",
     "core_23", "BoG", "GH"),
    ("inst-global-access", "Global Access Savings and Loans Company Limited", "", "core_23", "BoG", "GH"),
    ("inst-gn", "GN Savings and Loans Ltd.", "GN Bank[former];GN[variant]", "core_23", "BoG", "GH"),
    ("inst-ideal-finance", "Ideal Finance Limited", "IFL[variant]", "core_23", "BoG", "GH"),
    ("inst-ifs", "IFS Financial Services Limited", "", "core_23", "BoG", "GH"),
    ("inst-legacy-capital", "Legacy Capital Savings and Loans Ltd.", "", "core_23", "BoG", "GH"),
    ("inst-midland", "Midland Savings and Loans Company Limited", "", "core_23", "BoG", "GH"),
    ("inst-sterling", "Sterling Financial Services Limited", "", "core_23", "BoG", "GH"),
    ("inst-unicredit", "uniCredit Ghana Limited",
     "Kantamanto Savings and Loans Company Limited[former];uniCredit Savings & Loans Ltd.[variant]",
     "core_23", "BoG", "GH"),
    ("inst-wwbg", "Women's World Banking Ghana (WWBG) Savings and Loans Limited",
     "WWBG[variant]", "core_23", "BoG", "GH"),
]

NAMED_OTHERS = [
    ("corp-alltime-capital", "AllTime Capital Limited", "", "counterparty", "unknown", "GH"),
    ("corp-ivory-finance", "Ivory Finance Company Limited", "", "counterparty", "unknown", "GH"),
    ("corp-first-african-remittances", "First African Remittances, UK", "", "counterparty", "unknown", "UK"),
    ("corp-ghana-growth-fund", "Ghana Growth Fund", "Gold Coast Advisors[variant]", "counterparty", "SEC", "GH"),
    ("corp-gold-coast-fund-management", "Gold Coast Fund Management Limited",
     "Blackshield Capital Management[later]", "counterparty", "SEC", "GH"),
    ("corp-ideal-capital-partners", "Ideal Capital Partners", "", "counterparty", "unknown", "GH"),
    ("corp-unisecurities", "uniSecurities Limited", "", "counterparty", "SEC", "GH"),
    ("corp-liberty-asset-management", "Liberty Asset Management", "", "counterparty", "unknown", "GH"),
    ("corp-liberty-dmi-microfinance", "Liberty DMI Microfinance", "", "counterparty", "BoG", "GH"),
    ("corp-international-business-solutions", "International Business Solutions", "",
     "counterparty", "none", "US"),
    ("corp-griffin-financial-services", "Griffin Financial Services", "", "counterparty", "unknown", "GH"),
    ("hold-groupe-nduom", "Groupe Nduom", "Groupe Ndoum[typo];Groupe Nduom network companies[variant]", "counterparty", "none", "GH"),
    ("hold-ideal-financial-holdings", "Ideal Financial Holdings", "", "counterparty", "none", "GH"),
    ("hold-nordcom-africa-holdings", "Nordcom Africa Holdings Limited", "", "counterparty", "none", "unknown"),
    ("hold-hoda-group", "Hoda Group of Companies", "", "counterparty", "none", "GH"),
]

ENTITY_TYPE = {
    "hold-ideal-financial-holdings": "holding_company",
    "hold-nordcom-africa-holdings": "holding_company",
    "hold-hoda-group": "holding_company",
    "hold-groupe-nduom": "holding_company",
}

# Placeholders. member_count is only populated where the notice states a number.
# (entity_id, canonical_name, entity_type, member_count)
PLACEHOLDERS = [
    ("ph-accent-related-parties", "UNNAMED related parties of Accent", "placeholder_group", ""),
    ("ph-adom-related-parties", "UNNAMED related parties of Adom", "placeholder_group", ""),
    ("ph-alltime-related-companies", "UNNAMED related companies of AllTime", "placeholder_group", ""),
    ("ph-asn-related-parties", "UNNAMED related party projects of ASN", "placeholder_group", ""),
    ("ph-cdh-affiliates", "UNNAMED affiliates of CDH", "placeholder_group", ""),
    ("ph-crest-parent", "UNNAMED parent company of Crest", "placeholder_group", "1"),
    ("ph-crest-ceo-company", "UNNAMED company in which the Crest CEO is a director",
     "placeholder_group", "1"),
    ("ph-dream-6", "UNNAMED six related companies of Dream", "placeholder_group", "6"),
    ("ph-express-related-parties", "UNNAMED related parties of Express", "placeholder_group", ""),
    ("ph-first-allied-shareholder", "UNNAMED major shareholder of First Allied", "person", ""),
    ("ph-first-allied-8", "UNNAMED eight related companies of First Allied", "placeholder_group", "8"),
    ("ph-first-african-related-parties", "UNNAMED related parties of First African",
     "placeholder_group", ""),
    ("ph-firstrust-6", "UNNAMED six related companies of FirsTrust", "placeholder_group", "6"),
    ("ph-global-access-shareholder", "UNNAMED majority shareholder of Global Access", "person", ""),
    ("ph-ideal-affiliates", "UNNAMED affiliates of Ideal Finance", "placeholder_group", ""),
    ("ph-legacy-related-parties", "UNNAMED related parties of Legacy Capital", "placeholder_group", ""),
    ("ph-gn-related-parties", "UNNAMED related parties of GN in the Groupe Nduom network",
     "placeholder_group", ""),
]

# Maps the free-text names in the Phase 0 candidate sheet onto entity ids.
NAME_TO_ID = {}
for eid, name, *_ in INSTITUTIONS + NAMED_OTHERS:
    NAME_TO_ID[name] = eid
NAME_TO_ID.update({
    # Phase 0 wrote these names slightly differently.
    "CDH Savings and Loans Limited": "inst-cdh",
    "Legacy Capital Savings and Loans Limited": "inst-legacy-capital",
    "GN Savings and Loans Limited": "inst-gn",
    "Alpha Capital Savings and Loans Limited": "inst-alpha-capital",
    "Ghana Growth Fund (Gold Coast Advisors)": "corp-ghana-growth-fund",
    "Groupe Nduom network companies": "hold-groupe-nduom",
    "International Business Solutions": "corp-international-business-solutions",
    "Gold Coast Fund Management Limited (now Blackshield Capital Management)":
        "corp-gold-coast-fund-management",
    "UNNAMED related parties of Accent": "ph-accent-related-parties",
    "UNNAMED related parties of Adom": "ph-adom-related-parties",
    "UNNAMED related companies of AllTime": "ph-alltime-related-companies",
    "UNNAMED related party projects of ASN": "ph-asn-related-parties",
    "UNNAMED affiliates of CDH": "ph-cdh-affiliates",
    "UNNAMED parent company of Crest": "ph-crest-parent",
    "UNNAMED company in which the Crest CEO is a director": "ph-crest-ceo-company",
    "UNNAMED six related companies of Dream": "ph-dream-6",
    "UNNAMED related parties of Express": "ph-express-related-parties",
    "UNNAMED major shareholder of First Allied": "ph-first-allied-shareholder",
    "UNNAMED eight related companies of First Allied": "ph-first-allied-8",
    "UNNAMED related parties of First African": "ph-first-african-related-parties",
    "UNNAMED six related companies of FirsTrust": "ph-firstrust-6",
    "UNNAMED majority shareholder of Global Access": "ph-global-access-shareholder",
    "UNNAMED affiliates of Ideal Finance": "ph-ideal-affiliates",
    "UNNAMED related parties of Legacy Capital": "ph-legacy-related-parties",
    "UNNAMED related parties of GN in the Groupe Nduom network": "ph-gn-related-parties",
})

# Roles are evidenced by the same passages as these edges. Deriving the anchor
# rather than hardcoding it means a corrected anchor stays correct everywhere.
ROLE_ANCHOR_FROM_EDGE = {"R001": "E014", "R002": "E019", "R003": "E010"}

# Renamings from the Phase 0 sheet that become aliases, not edges.
RENAMING_EDGES = {"E033", "E035", "E036", "E038"}

# amount_basis for the Phase 0 amounts, read off the wording of each passage.
AMOUNT_BASIS = {
    "E014": ("floor", "notice says 'in excess of' GHS 100.00 million"),
    "E018": ("exact", "projected cash injection for the proposed merger, not an exposure"),
    "E022": ("combined_total", "GHS 761.55m is stated across E022 and E023 together"),
    "E023": ("combined_total", "GHS 761.55m is stated across E022 and E023 together"),
    "E024": ("combined_total", "GHS 63.19m is stated across E024 and E025 together"),
    "E025": ("combined_total", "GHS 63.19m is stated across E024 and E025 together"),
    "E026": ("exact", "total related party loans; reconcile against the GHS 63.19m figure"),
}

RELATIONSHIP_TYPES = [
    ("owns", "ownership", "0", "Holds an ownership interest in the target."),
    ("acquired", "ownership", "0", "Took ownership of the target on a stated date."),
    ("part_of", "ownership", "0", "Is a member of the target group or holding structure."),
    ("controls", "ownership", "0", "Exercises control without a stated shareholding figure."),
    ("directs", "governance", "0", "Holds a directorship or board position at the target."),
    ("lends_to", "lending", "1", "Extended credit to the target."),
    ("over_exposed_to", "lending", "1",
     "Credit exposure to the target beyond the regulatory limit."),
    ("related_party_exposure_to", "lending", "1",
     "Exposure the source document classifies as related-party."),
    ("placed_funds_with", "placement", "1",
     "Placed institutional or depositor funds with the target."),
    ("holds_deposits_in", "placement", "1", "Holds deposits or investments in the target."),
    ("overdrawn_current_accounts", "lending", "1",
     "Target's current accounts with the institution were overdrawn."),
    ("extended_overdraft_facilities_to", "lending", "1",
     "Extended overdraft and similar facilities to the target."),
    ("funded_projects_of", "lending", "1",
     "Used depositor funds to finance projects of the target."),
    ("transferred_collateral_to", "lending", "1",
     "Transferred collateral security to the target with no cash inflow."),
    ("pays_management_fees_to", "fee_extraction", "1",
     "Pays management fees to the target."),
    ("pays_rent_to", "fee_extraction", "1", "Pays rent or premises costs to the target."),
    ("assumed_liability_of_loan_of", "fee_extraction", "1",
     "Took onto its own books a loan contracted by the target."),
    ("pre_financed_receivable_from", "placement", "1",
     "Pre-financed a receivable the target failed to reimburse."),
    ("transferred_funds_to", "placement", "1",
     "Transferred depositor funds to the target."),
    ("proposed_merger_with", "corporate_action", "0",
     "Applied to merge operations with the target."),
    ("succeeded", "corporate_action", "0",
     "Took over the business of the target as a going concern."),
]

SOURCES = [
    (SOURCE_ID,
     "Notice of revocation of licences of 23 savings and loans companies and finance houses",
     "Bank of Ghana", "2019-08-16", "revocation_notice",
     "https://www.bog.gov.gh/", f"sources/{SOURCE_ID}.pdf", TODAY,
     "Text extracted from the published PDF; the cedi sign does not survive extraction "
     "and is normalised to GHS in the working text."),
    ("bog-2019-05-31-microfinance-revocation",
     "Notice of revocation of licences of microfinance institutions",
     "Bank of Ghana", "2019-05-31", "revocation_notice",
     "https://www.bog.gov.gh/", "(held in ghana-banking-collapse)", TODAY,
     "Out of scope as nodes. Used once for corroboration: Liberty DMI Microfinance "
     "appears as entry 109."),
    ("ghana-banking-collapse-verified",
     "Verified savings & loans dataset", "Samuel Ato Kwame Baah", "2026-08-29", "dataset",
     "https://doi.org/10.5281/zenodo.22163244",
     "(held in ghana-banking-collapse: data/savings_loans_verified.csv)", TODAY,
     "Source of institution_attributes. Not retyped."),
]


def build_evidence_index():
    """anchor -> verbatim block text, for every bullet in the notice."""
    lines = read_lines()
    index = {}
    for line_no, block in blocks(lines, 0, len(lines)):
        index[f"{SOURCE_ID}:L{line_no}"] = tidy(block)
    return index


def write_csv(name, header, rows):
    path = DATA / name
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"  {name:26} {len(rows):>4} rows")
    return path


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    evidence_index = build_evidence_index()
    candidates = list(csv.DictReader(CANDIDATES.open(encoding="utf-8")))

    # ---- sources ----
    write_csv("sources.csv",
              ["source_id", "title", "publisher", "published_date", "doc_type",
               "url", "local_path", "retrieved_date", "notes"],
              SOURCES)

    # ---- relationship_types ----
    write_csv("relationship_types.csv",
              ["relationship", "category", "extracts_value", "description"],
              RELATIONSHIP_TYPES)

    # ---- entities ----
    ent_rows = []
    for eid, name, aka, scope, reg, juris in INSTITUTIONS + NAMED_OTHERS:
        etype = ENTITY_TYPE.get(eid, "institution" if eid.startswith("inst-") else "corporate_entity")
        ent_rows.append([eid, name, etype, aka, scope, reg, juris, "", "1", "", "", ""])
    for eid, name, etype, count in PLACEHOLDERS:
        ent_rows.append([eid, name, etype, "", "placeholder", "none", "GH", count, "0", "", "", ""])
    write_csv("entities.csv",
              ["entity_id", "canonical_name", "entity_type", "also_known_as", "scope_class",
               "regulator", "jurisdiction", "member_count", "is_named",
               "admitted_by_edge_id", "evidence_anchors", "notes"],
              ent_rows)

    # ---- evidence + edges ----
    used_anchors, edge_rows, unresolved = {}, [], []
    for c in candidates:
        if c["edge_id"] in RENAMING_EDGES:
            continue  # becomes an alias on the entity instead
        src = NAME_TO_ID.get(c["source_entity"])
        tgt = NAME_TO_ID.get(c["target_entity"])
        if src is None:
            unresolved.append((c["edge_id"], "source", c["source_entity"]))
        if tgt is None:
            unresolved.append((c["edge_id"], "target", c["target_entity"]))

        anchor = ""
        if c["source_anchor"]:
            anchor = f"{SOURCE_ID}:{c['source_anchor']}"
            if anchor in evidence_index:
                used_anchors[anchor] = evidence_index[anchor]
            else:
                unresolved.append((c["edge_id"], "anchor", anchor))

        basis, basis_note = AMOUNT_BASIS.get(c["edge_id"], ("", ""))
        if c["amount_ghs_m"] and not basis:
            basis = "exact"
        edge_rows.append([
            c["edge_id"], src or "UNRESOLVED", tgt or "UNRESOLVED", c["relationship"],
            c["amount_ghs_m"], "GHS" if c["amount_ghs_m"] else "", 
            "million" if c["amount_ghs_m"] else "",
            basis, basis_note, "", c["confidence"], anchor,
            c["review_note"], VERSION, "",
        ])

    write_csv("edges.csv",
              ["edge_id", "source_entity_id", "target_entity_id", "relationship",
               "amount_value", "amount_currency", "amount_unit", "amount_basis",
               "amount_note", "as_at_date", "confidence", "evidence_anchors",
               "review_note", "version_added", "version_removed"],
              edge_rows)

    # ---- roles ----
    by_edge = {c["edge_id"]: c for c in candidates}

    def role_anchor(role_id):
        c = by_edge[ROLE_ANCHOR_FROM_EDGE[role_id]]
        anchor = f"{SOURCE_ID}:{c['source_anchor']}"
        used_anchors.setdefault(anchor, evidence_index[anchor])
        return anchor

    write_csv("roles.csv",
              ["role_id", "entity_id", "institution_id", "role_type", "start_date",
               "end_date", "confidence", "evidence_anchors", "notes"],
              [
                  ["R001", "ph-first-allied-shareholder", "inst-first-allied",
                   "majority_shareholder", "", "", "documented_unnamed",
                   role_anchor("R001"),
                   "Eight related companies are linked to this shareholder; identity not stated"],
                  ["R002", "ph-global-access-shareholder", "inst-global-access",
                   "majority_shareholder", "", "", "documented_unnamed",
                   role_anchor("R002"), "Role stated; identity not"],
                  ["R003", "ph-crest-ceo-company", "inst-crest", "ceo", "", "",
                   "documented_unnamed", role_anchor("R003"),
                   "The Crest CEO is a director of this company; both unnamed"],
              ])

    write_csv("evidence.csv",
              ["anchor", "source_id", "quote", "page", "extracted_date"],
              [[a, SOURCE_ID, q, "", TODAY] for a, q in sorted(used_anchors.items())])

    # ---- resolution review ----
    write_csv("resolution_review.csv",
              ["candidate_id", "name_a", "entity_id_a", "name_b", "entity_id_b",
               "similarity", "reason", "decision", "decided_date", "decision_note"],
              [
                  ["RR001", "Sterling Savings and Loans Limited", "inst-commerz",
                   "Sterling Financial Services Limited", "inst-sterling", "0.62",
                   "Commerz is described as formerly known as Sterling Savings and Loans "
                   "Limited; Sterling Financial Services is separately institution 21",
                   "undecided", "", "Needs a source. Changes the graph either way"],
                  ["RR002", "Ivory Finance Company Limited", "corp-ivory-finance",
                   "CDH Savings and Loans Ltd.", "inst-cdh", "0.10",
                   "CDH commenced operations after taking over Ivory Finance. Predecessor "
                   "alias of the same legal person, or a distinct entity acquired?",
                   "undecided", "", "Currently modelled as a distinct entity with a succeeded edge"],
                  ["RR003", "Ideal Financial Holdings", "hold-ideal-financial-holdings",
                   "Ideal Finance Limited", "inst-ideal-finance", "0.71",
                   "Shared name suggests common ownership; no source in hand states it",
                   "undecided", "", "Held as inferred edge I001, excluded from headline findings"],
              ])

    # ---- changelog ----
    write_csv("changelog.csv",
              ["change_id", "version", "change_date", "change_type", "object_type",
               "object_id", "reason", "source_id"],
              [["C001", VERSION, TODAY, "add", "batch", "phase0-seed",
                "Initial seed reshaped from the Phase 0 candidate sheet. Every row is a "
                "first pass awaiting hand verification against the notice.", SOURCE_ID],
               ["C002", VERSION, TODAY, "correct", "batch", "line-anchors",
                "Every line anchor corrected. The Phase 0 extractor used str.splitlines(), "
                "which also breaks on form feeds; this notice carries 27 of them as page "
                "breaks, so anchors ran up to 26 lines ahead of what grep, sed or an editor "
                "shows. Anchors now match the line a reader sees. E021-E023 were also "
                "pointing at the wrong paragraph and were moved to L798.", SOURCE_ID],
               ["C003", VERSION, TODAY, "add", "batch", "groupe-nduom-ibs",
                "Added International Business Solutions and the Groupe Nduom ownership "
                "edge, from a passage the extractor had missed because its ownership "
                "pattern matched 'owner' and 'ownership' but not 'owned'.", SOURCE_ID]])

    print(f"\nedges written: {len(edge_rows)}  "
          f"(4 renaming rows folded into entity aliases)")
    if unresolved:
        print(f"\nUNRESOLVED ({len(unresolved)}) - fix before loading:")
        for edge_id, field, value in unresolved:
            print(f"  {edge_id} {field}: {value}")
    else:
        print("all edge endpoints and anchors resolved")


if __name__ == "__main__":
    main()
