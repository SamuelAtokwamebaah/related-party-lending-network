"""
v0.7 - corrections from the pre-release audit of 13 September 2026.

Before the repository went public, every edge was re-read against its passage,
every number in the prose was recounted from the CSVs, the pipeline was rebuilt
from a clean clone, and the loader was fed deliberately broken data. This script
applies the corrections to the evidence base. Code and prose corrections are in
the same commit; the reasons for each are in data/changelog.csv, C028 to C040.

What changed, in order of consequence:

- E013 pointed the wrong way. It said First Allied controls its own majority
  shareholder. The notice names a "Board Chairman/Majority Shareholder" of the
  institution (L543): the shareholder owns the institution.
- E019 and E020 were classed `documented`, but their counterparty is the unnamed
  majority shareholder of Global Access. By the schema's own definition they are
  `documented_unnamed`, which changes the published confidence counts.
- E002 and E016 used a relationship stronger or looser than the text. E002's
  exposures are stated to exceed the statutory limit; E016's are exposure of an
  unstated form.
- Five relationships stated in the notice had no edge, although identical wording
  produced an edge for another institution: GN's exposure above the 25% limit,
  CDH's placements with related companies, Crest's parent company, and Dream and
  FirsTrust using depositors' funds for related-party projects.
- R003 recorded a company as Crest's chief executive. It is removed; the fact is
  kept in E010's note. First Allied's placeholder shareholder gains the board
  chairman role the notice states.
- Ghana Growth Fund was recorded as SEC-regulated on the Bank of Ghana's word,
  although the SEC itself calls it an unregulated related entity.
- RR001 is closed as `different`: the notice lists Commerz and Sterling Financial
  Services as two licensees, revoked separately on the same day.

Every edge whose relationship, direction, confidence, anchor, amount or date
changed is set back to `pending`, with its earlier decision kept in the note, so
the evidence base says plainly that it has not yet been re-checked by hand.

Usage:  python scripts/integrate_audit_v07.py
"""

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
VERSION = "v0.7"
TODAY = "2026-09-13"
BOG = "bog-2019-08-16-savings-loans-revocation"
SEC = "sec-2019-11-08-fund-manager-revocation"
CA = "ca-2026-05-21-gn-savings-appeal"


def load(name):
    with (DATA / name).open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader), reader.fieldnames


def save(name, rows, fields):
    with (DATA / name).open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def superseded_by():
    """The latest version in the changelog, if it is later than this script's."""
    with (DATA / "changelog.csv").open(encoding="utf-8", newline="") as fh:
        versions = {r["version"] for r in csv.DictReader(fh)}
    key = lambda v: tuple(int(x) for x in v.lstrip("v").split("."))
    later = sorted((v for v in versions if key(v) > key(VERSION)), key=key)
    return later[-1] if later else None


def bog_quote(line_no, ends_with):
    """A verbatim quote from the notice, starting at line_no and ending at a phrase.

    Taken from the working text rather than typed, so it is verbatim by
    construction. The cedi sign is normalised as the loader normalises it, and a
    leading list marker or bullet is dropped, as in every other quote here.
    """
    text = (DATA / "raw" / f"{BOG}.txt").read_text(encoding="utf-8")
    text = text.replace("�", "GHS ").replace("GHGHS ", "GHS ").replace("GHS  ", "GHS ")
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    window = " ".join(l for l in lines[line_no - 1: line_no + 40]
                      if not re.match(r"^\s*\d{1,3}\s*$", l))
    window = re.sub(r"\s+", " ", window).strip()
    window = re.sub(r"^[^\w]+", "", window)
    window = re.sub(r"^(?:[a-z]|\d{1,2})[.)]\s+", "", window)
    end = window.index(ends_with) + len(ends_with)
    return window[:end]


# --- evidence --------------------------------------------------------------------
EVIDENCE = [
    (381, "worsened its solvency liquidity situation."),
    (543, "Management of the Institution"),
    (826, "made by the bank on behalf of such affiliates."),
    (929, "FirsTrust Savings and Loans Limited (FTSL)."),
    (1108, "a sister company."),
]

# --- edges: field changes --------------------------------------------------------
# (edge_id, changes, needs_recheck, what changed)
EDGE_CHANGES = [
    ("E002", {"relationship": "over_exposed_to",
              "review_note": "Exposures stated to be far in excess of the statutory limits; no "
                             "amount stated. Shares Adom's placeholder with E003, although the "
                             "notice does not say the fee recipients and these counterparties "
                             "are the same parties"},
     True, "relationship lends_to -> over_exposed_to: the passage states a breach of the "
           "statutory limit and does not say the exposure is lending"),
    ("E003", {"review_note": "Management fees paid to related parties; no amount stated. See "
                             "E002 on the shared placeholder"}, False, ""),
    ("E007", {"review_note": "Collateral transferred to affiliates with no cash inflow; the notice "
                             "frames it as an overstatement of the balance sheet"}, False, ""),
    ("E010", {"review_note": "Exposure to a company in which Crest's chief executive is a "
                             "director; neither the company nor the chief executive is named"},
     False, ""),
    ("E013", {"source_entity_id": "ph-first-allied-shareholder",
              "target_entity_id": "inst-first-allied",
              "relationship": "owns",
              "evidence_anchors": f"{BOG}:L543",
              "review_note": "Stated as the institution's Board Chairman/Majority Shareholder "
                             "(L543); identity and shareholding not stated"},
     True, "direction reversed and relationship controls -> owns: the edge said First Allied "
           "controls its own majority shareholder; L543 names the Board Chairman/Majority "
           "Shareholder of the institution. Anchor moved from L580, which does not state the "
           "relationship, to L543"),
    ("E016", {"relationship": "related_party_exposure_to",
              "review_note": "Related party exposure the institution is unable to recover; its "
                             "form is not stated. May overlap E015"},
     True, "relationship lends_to -> related_party_exposure_to: the passage does not say the "
           "exposure is lending"),
    ("E018", {"amount_note": "Projected cash injection of GHS 127.00m into the merged entity, if "
                             "approved; not a flow between the two parties",
              "evidence_anchors": f"{BOG}:L702; {BOG}:L929",
              "review_note": "Notification letter dated 25 June 2019 (L929); the refusal cites a "
                             "request dated 25 July 2019 (L702). Refused, both being insolvent"},
     True, "anchor L929 added for the 25 June 2019 letter; notes separate the letter's date "
           "from the request's"),
    ("E019", {"confidence": "documented_unnamed",
              "review_note": "Loan contracted by the majority shareholder, concealed in a "
                             "suspense account; the shareholder is not named"},
     True, "confidence documented -> documented_unnamed: the counterparty is the unnamed "
           "majority shareholder"),
    ("E020", {"confidence": "documented_unnamed",
              "evidence_anchors": f"{BOG}:L741",
              "review_note": "Rent paid to the majority shareholder for the use of its premises; "
                             "no amount stated"},
     True, "confidence documented -> documented_unnamed; section-heading anchor L713, added only "
           "to satisfy rule 12 for a named counterparty, removed"),
    ("E026", {"as_at_date": "2017-09",
              "amount_note": "Total related party loans per the onsite examination of September "
                             "2017 (L913); the GHS 63.19m on E024 and E025 is a later figure"},
     True, "as_at_date 2017-09 added: the figure comes from the September 2017 onsite "
           "examination, which explains why it differs from the GHS 63.19m"),
    ("E032", {"evidence_anchors": f"{BOG}:L1127; {BOG}:L1100; {BOG}:L1108"},
     True, "anchor L1108 added: it is the passage that states the over-exposure to "
           "uniSecurities, a sister company"),
    ("E034", {"review_note": "Holding company named in the notice. 'Formerly' may govern 'part of' "
                             "as well as the name, so current membership is not certain"},
     False, ""),
    ("E044", {"review_note": "Stated as undisputed by the Court of Appeal (p.14). The judgment "
                             "writes '3rd respondent'; the title of the suit (p.1) fixes that as "
                             "GN. Its introduction (pp.1-2, transcription L39) says the membership "
                             "lasted until the receivership. The Bank of Ghana notice implies it "
                             "('other companies in the Groupe Ndoum network', L798; 'another "
                             "company owned by Groupe Nduom', L840) but does not state it in "
                             "terms. First edge attributed to a court"}, False, ""),
    ("I002", {"review_note": "INFERRED. uniSecurities is uniCredit's 'sister company' (L1108) and "
                             "the Hoda Group of Companies acquired uniCredit in 2006 (L1104); no "
                             "source names uniSecurities' parent or states that Hoda held uniCredit "
                             "in 2019. Excluded from every figure"}, False, ""),
    ("S005", {"amount_note": "9.45% of its funds; a ratio, not an amount"}, False, ""),
    ("S006", {"amount_note": "10.93% of its funds; a ratio, not an amount"}, False, ""),
    ("S014", {"as_at_date": "2018-06-30",
              "amount_note": "99.41% of funds under management per the 2nd Quarter 2018 "
                             "placement report; a ratio, not an amount",
              "review_note": "The Bank of Ghana names both as sister companies of GN and calls "
                             "them SEC-licensed; the Commission calls Ghana Growth Fund an "
                             "unregulated related entity"},
     True, "as_at_date 2018-06-30 added from the 2nd Quarter 2018 placement report"),
    ("P011", {"review_note": "A second passage of the same notice placing client funds with "
                             "Commerz; no related-party claim, so it does not bear on the "
                             "related-party flag"}, False, ""),
]

UNISEC_NOTE = ("The Commission lists these as related parties inside a finding on placement of "
               "client funds; it does not state that funds were placed with each, or any amount. "
               "That the Commission's Unisecurities (Ghana) Limited is the Bank of Ghana's "
               "uniSecurities rests on the name; see LIMITATIONS section 10")
for eid in ("S007", "S008", "S009", "S010", "S011", "S012", "S013"):
    note = UNISEC_NOTE
    if eid == "S007":
        note += ". Whether Hoda Holdings Ltd is the Hoda Group of Companies that acquired uniCredit is undecided; see RR004"
    EDGE_CHANGES.append((eid, {"review_note": note}, False, ""))

INTEGRITY_NOTE = ("Stated as 'Over 80% placement of client funds in revoked savings & loans "
                  "including' Midland, FirsTrust and Legacy Capital. The notice gives no "
                  "per-institution split, the figure is a floor, and 'including' leaves the list "
                  "open.")
for eid in ("P007", "P008", "P009"):
    EDGE_CHANGES.append((eid, {"amount_note": INTEGRITY_NOTE}, False, ""))

NEW_EDGES = [
    {"edge_id": "E045", "source_entity_id": "inst-cdh",
     "target_entity_id": "ph-cdh-related-companies", "relationship": "placed_funds_with",
     "confidence": "documented_unnamed", "evidence_anchors": f"{BOG}:L381",
     "review_note": "Placements/investments with related companies that CDH could not access; "
                    "count and amount not stated. Held apart from ph-cdh-affiliates, because "
                    "the notice says 'related companies' here and 'affiliate companies' "
                    "elsewhere and does not say they are the same"},
    {"edge_id": "E046", "source_entity_id": "inst-gn",
     "target_entity_id": "ph-gn-related-parties", "relationship": "over_exposed_to",
     "confidence": "documented_unnamed", "evidence_anchors": f"{BOG}:L826",
     "review_note": "Exposure to its related party consistently above the 25% limit of net "
                    "own funds; other affiliate exposures were mainly payments made on their "
                    "behalf. The same wording produced E024 and E025 for Ideal Finance"},
    {"edge_id": "E047", "source_entity_id": "ph-crest-parent",
     "target_entity_id": "inst-crest", "relationship": "owns",
     "confidence": "documented_unnamed", "evidence_anchors": f"{BOG}:L434",
     "review_note": "'its parent company'; identity and shareholding not stated"},
    {"edge_id": "E048", "source_entity_id": "inst-dream",
     "target_entity_id": "ph-dream-6", "relationship": "funded_projects_of",
     "confidence": "documented_unnamed", "evidence_anchors": f"{BOG}:L472",
     "review_note": "'The use of depositors' funds to finance related party projects', the "
                    "wording that produced E031 for ASN. The notice does not say the projects "
                    "belong to the six related companies of E011; attached to Dream's "
                    "related-party placeholder, as E002 and E003 share Adom's"},
    {"edge_id": "E049", "source_entity_id": "inst-firstrust",
     "target_entity_id": "ph-firstrust-6", "relationship": "funded_projects_of",
     "confidence": "documented_unnamed", "evidence_anchors": f"{BOG}:L685",
     "review_note": "'The use of depositors' funds to finance related party projects', the "
                    "wording that produced E031 for ASN. The notice does not say the projects "
                    "belong to the six related companies of E017; attached to FirsTrust's "
                    "related-party placeholder, as E002 and E003 share Adom's"},
]

# --- entities --------------------------------------------------------------------
ALIASES = {
    "inst-dream": ["El Finance Limited[later]"],
    "inst-first-ghana": ["First Ghana Building Society[former]",
                         "First Ghana Building Company Limited[former]"],
    "inst-gn": ["First National Savings and Loans (FNSL) Company Limited[former]"],
    "inst-legacy-capital": ["Legacy Capital Savings Limited[variant]"],
    "inst-firstrust": ["Firstrust Savings and Loans[variant]"],
    "corp-ghana-growth-fund": ["Ghana Growth Fund Limited[variant]"],
    "corp-ideal-capital-partners": ["Ideal Capital Partners Limited[variant]"],
    "corp-liberty-asset-management": ["Liberty Asset Management Limited[variant]"],
    "corp-unisecurities": ["Unisecurities (Ghana) Limited[variant]"],
}

ENTITY_CHANGES = {
    "ph-asn-related-parties": {"canonical_name": "UNNAMED related parties of ASN"},
    "ph-global-access-shareholder": {
        "entity_type": "placeholder_group", "member_count": "1",
        "notes": "The notice says 'majority shareholder' only, and does not say whether it is a "
                 "person or a company"},
    "ph-first-allied-shareholder": {
        "notes": "A person: the notice names the same party as Board Chairman (L543)"},
    "corp-ghana-growth-fund": {
        "regulator": "unknown",
        "notes": "The Bank of Ghana (L804) calls it licensed by the Securities and Exchange "
                 "Commission; the Commission (L673) calls Ghana Growth Fund Limited an "
                 "unregulated related entity"},
    "corp-ideal-capital-partners": {"regulator": "SEC"},
    "corp-liberty-asset-management": {"regulator": "SEC"},
    "corp-international-business-solutions": {"regulator": "unknown"},
}

NEW_ENTITIES = [
    {"entity_id": "ph-cdh-related-companies",
     "canonical_name": "UNNAMED related companies of CDH",
     "entity_type": "placeholder_group", "scope_class": "placeholder", "regulator": "none",
     "jurisdiction": "GH", "is_named": "0"},
]

UK_NOTE_OLD = ("Its strike-off, the Registrar's suspension of that strike-off on an objection, "
               "and its dissolution are evidenced by the Registrar's own notices, vendored in "
               "sources/.")
UK_NOTE_NEW = ("The first Gazette notice, the Registrar's suspension of the strike-off on an "
               "objection, and the dissolution are the Registrar's own notices, vendored in "
               "sources/. Two dates rest on the register transcription only: the strike-off "
               "application of 30 May 2019, and 4 July 2019 for the suspension, whose notice "
               "carries no date.")

# --- roles -----------------------------------------------------------------------
ROLE_CHANGES = {
    "R001": {"evidence_anchors": f"{BOG}:L543; {BOG}:L580",
             "notes": "Board Chairman/Majority Shareholder (L543); eight related companies are "
                      "linked to this shareholder (L580). Identity not stated"},
}
ROLES_REMOVED = ["R003"]
NEW_ROLES = [
    {"role_id": "R004", "entity_id": "ph-first-allied-shareholder",
     "institution_id": "inst-first-allied", "role_type": "board_chairman",
     "confidence": "documented_unnamed", "evidence_anchors": f"{BOG}:L543",
     "notes": "The same party is named Board Chairman and Majority Shareholder (L543). "
              "Identity not stated"},
]

# --- resolution ------------------------------------------------------------------
RESOLUTION_CHANGES = {
    "RR001": {"decision": "different", "decided_date": TODAY,
              "decision_note": "Different entities, on the notice itself: it lists Commerz "
                               "(institution 7, licensed December 2016) and Sterling Financial "
                               "Services (institution 21, licensed 1997) as two licensees, "
                               "revoked separately on the same day. Commerz's former name is "
                               "Sterling Savings and Loans Limited. Whether the two were related "
                               "is not documented, and no edge is drawn"},
    "RR005": {"reason": "Section 16 of Appendix B of the SEC notice (Intermarket, formerly CDH "
                        "Asset Management) shares the CDH name with institution 6. The section "
                        "says over 40% of client funds were placed in its parent company, CDH "
                        "Investment Holdings; nothing in hand connects either to CDH Savings and "
                        "Loans. Shared naming only."},
    "RR006": {"entity_id_a": "fm-legacy-fund-management"},
}
RR007_REPLACE = [
    ("with two directors recorded as Ghanaian nationals resident in Accra",
     "with two directors recorded as Ghanaian nationals resident in Ghana, with a correspondence "
     "address in Accra"),
    ("two months after the licence was revoked over GHS 5.40m the affiliate had not reimbursed",
     "two months after the licence was revoked in a notice that cites, among other issues, "
     "GHS 5.40m the affiliate had not reimbursed"),
]

# --- relationship types ----------------------------------------------------------
REL_CHANGES = {
    "pays_management_fees_to": {"category": "payments"},
    "pays_rent_to": {"category": "payments"},
    "assumed_liability_of_loan_of": {"category": "payments"},
    "placed_funds_with": {"description": "Placed institutional, depositor or client funds with "
                                         "the target."},
}

# --- changelog -------------------------------------------------------------------
CHANGELOG = [
    ("C028", "correct", "note", "C009",
     "C009 miscounted. Of the four SEC sections read at v0.3, two name one of the 23, so nine "
     "unread sections named one of the 23, not eight. The nine fund managers C009 lists were "
     "right; the arithmetic in its last sentence was not. Corrected everywhere the count appears.",
     SEC),
    ("C029", "correct", "edge", "E013",
     "Direction reversed. The edge said First Allied controls its own majority shareholder. The "
     "notice names the institution's Board Chairman/Majority Shareholder (L543), so the "
     "shareholder owns the institution. Relationship controls -> owns, anchor L580 -> L543.", BOG),
    ("C030", "correct", "batch", "E019;E020",
     "Confidence documented -> documented_unnamed. Both run to the unnamed majority shareholder of "
     "Global Access, a placeholder. Documented edges now 48, documented_unnamed 20 before the "
     "edges added in C032. E020's heading anchor, added only to satisfy rule 12, is removed.", BOG),
    ("C031", "correct", "batch", "E002;E016",
     "Relationship narrowed to what the text states. E002: lends_to -> over_exposed_to, because "
     "the passage states a breach of the statutory limit. E016: lends_to -> "
     "related_party_exposure_to, because the passage does not say what form the exposure took.",
     BOG),
    ("C032", "add", "batch", "E045;E046;E047;E048;E049",
     "Five relationships the notice states had no edge, although the same wording produced an "
     "edge for another institution. E045 CDH placements with related companies (L381), under a "
     "new placeholder; E046 GN's exposure above the 25% limit (L826), as for Ideal Finance; E047 "
     "Crest's parent company owns it (L434); E048 and E049 Dream and FirsTrust funding related "
     "party projects (L472, L685), as for ASN. All five are documented_unnamed and pending a "
     "hand check.", BOG),
    ("C033", "correct", "batch", "R001;R003;R004",
     "R003 recorded a company as Crest's chief executive. The notice (L434) says the chief "
     "executive is a director of that company; neither is named. R003 is removed and the fact is "
     "kept in E010's note. R004 adds the board chairman role the notice states for First Allied's "
     "majority shareholder (L543), and R001 now cites L543, where 'Majority Shareholder' appears.",
     BOG),
    ("C034", "correct", "batch", "entities",
     "Ghana Growth Fund regulator SEC -> unknown: the Bank of Ghana calls it SEC-licensed and the "
     "Commission calls it unregulated, and the record now says both. Ideal Capital Partners and "
     "Liberty Asset Management regulator -> SEC, as the Commission records their licences. "
     "International Business Solutions none -> unknown. The Global Access majority shareholder "
     "is no longer typed as a person, since the notice does not say. ASN's placeholder renamed "
     "from 'related party projects' to 'related parties'. Former and later names the notice "
     "states were added as aliases (El Finance, First Ghana Building Society and Building "
     "Company, First National Savings and Loans), with the spellings the SEC notice uses. "
     "FirstTrust is the notice's own spelling of a name, so its alias type is variant, not typo.",
     BOG),
    ("C035", "correct", "resolution", "RR001",
     "Closed as different, on the notice: Commerz and Sterling Financial Services are two "
     "licensees, listed and revoked separately on the same day, licensed in 2016 and 1997. The "
     "earlier note said the answer changed the graph either way; a 'different' decision changes "
     "nothing. RR005's reason now cites the right section and the parent company it names; "
     "RR006 now carries the entity id that has existed since v0.4; RR007 no longer says the "
     "directors were resident in Accra (the register says Ghana) or that the licence was revoked "
     "over GHS 5.40m (the notice cites it among other issues).", BOG),
    ("C036", "correct", "batch", "notes-and-dates",
     "Notes and dates corrected to the text. E018 separates the 25 June 2019 letter from the "
     "request dated 25 July 2019, and no longer presents the projected GHS 127.00m as a flow "
     "between the parties. E026 is dated September 2017, the onsite examination its figure "
     "comes from. S014 is dated 30 June 2018, from the placement report it cites. E032 now cites "
     "L1108, the passage stating the over-exposure. E007's 'asset-stripping pattern' and the "
     "'fee extraction' notes were interpretation, not the notice's words. E034, E044, I002, "
     "S005 to S013, P007 to P009 and P011 carry notes that no longer claim more than the text. "
     "I002 was described as a shared-name inference; it rests on a sibling relationship and a "
     "2006 acquisition, and says so.", BOG),
    ("C037", "correct", "policy", "cross-document-matching",
     "The rule for matching an entity across two documents is now written down (LIMITATIONS "
     "section 10). The same legal name, allowing for punctuation, case and a jurisdiction "
     "suffix, is treated as the same entity; a different name is resolved only on a document. "
     "Four fund managers were matched across the Bank of Ghana and SEC notices this way at v0.3 "
     "without the rule being stated. The weakest is uniSecurities, whose SEC section names "
     "neither uniCredit nor the Hoda Group; it is recorded as resting on the name.", SEC),
    ("C038", "correct", "relationship_types", "payments",
     "Category fee_extraction renamed payments. Management fees, rent and a shareholder's loan "
     "taken onto the institution's books are payments to a related party; 'extraction' is not "
     "the notice's word and claims a direction LIMITATIONS section 8 withdraws. The description "
     "of placed_funds_with now covers a fund manager's client funds.", ""),
    ("C039", "correct", "code", "load.py",
     "The loader's defences were tested with deliberately broken data and five faults passed. "
     "Rule 11 compared only the first 80 characters of a quote, or accepted it anywhere in the "
     "next 60 lines, so a word changed late in a long quote, an empty quote and an anchor placed "
     "a few lines early all passed; the whole quote must now start at its anchor. Rule 12 "
     "matched name fragments, so the alias 'GN' matched inside ordinary words; it now matches "
     "whole words. New checks refuse a non-numeric amount, an unknown version, a duplicate in "
     "any keyed table, a decision for an edge that does not exist, and a row with too few "
     "fields, and a schema rejection no longer leaves an empty database behind.", ""),
    ("C040", "correct", "code", "build_site.py",
     "The map credited every quoted passage to the Bank of Ghana, including 17 from the SEC "
     "notice and one from the Court of Appeal. Each passage now names its own source. The page "
     "also said it was built only from the Bank of Ghana notice, printed 'all edges verified' "
     "beside a provisional banner, and said the Commission linked Ideal Capital Partners to "
     "Ideal Finance, which it does not. All corrected, with accessible names for the diagrams.",
     ""),
]


def main():
    later = superseded_by()
    if later:
        print(f"The evidence base is already at {later}. This script applied {VERSION} and "
              "is kept as a record. Nothing written.")
        return 0
    print(f"applying the pre-release audit corrections at {VERSION}\n")

    # evidence
    rows, fields = load("evidence.csv")
    have = {r["anchor"] for r in rows}
    added = 0
    for line_no, ends in EVIDENCE:
        anchor = f"{BOG}:L{line_no}"
        if anchor in have:
            continue
        rows.append({"anchor": anchor, "source_id": BOG, "quote": bog_quote(line_no, ends),
                     "page": "", "extracted_date": TODAY})
        added += 1
    save("evidence.csv", rows, fields)
    print(f"  evidence            + {added}")

    # edges
    rows, fields = load("edges.csv")
    by_id = {r["edge_id"]: r for r in rows}
    recheck = {}
    for eid, changes, needs, what in EDGE_CHANGES:
        before = dict(by_id[eid])
        by_id[eid].update(changes)
        if needs and before != by_id[eid]:
            recheck[eid] = what
    for new in NEW_EDGES:
        if new["edge_id"] not in by_id:
            row = {f: new.get(f, "") for f in fields}
            row["version_added"] = VERSION
            rows.append(row)
            by_id[new["edge_id"]] = row
            recheck[new["edge_id"]] = "added in the pre-release audit"
    save("edges.csv", rows, fields)
    print(f"  edges               ~ {len(EDGE_CHANGES)} changed, "
          f"{len(NEW_EDGES)} added, {len(recheck)} to re-check")

    # verification: anything whose reading changed goes back to pending
    rows, fields = load("verification.csv")
    ver = {r["edge_id"]: r for r in rows}
    for eid, what in recheck.items():
        prior = ver.get(eid)
        was = (f" Previously {prior['decision']} on {prior['verified_date']} by "
               f"{prior['verified_by']}." if prior and prior["decision"] != "pending" else "")
        row = {"edge_id": eid, "decision": "pending", "verified_date": "", "verified_by": "",
               "note": f"Changed in the v0.7 pre-release audit: {what}.{was} Awaiting a "
                       "re-check against the source."}
        if prior:
            prior.update(row)
        else:
            rows.append(row)
    rows.sort(key=lambda r: r["edge_id"])
    save("verification.csv", rows, fields)
    print(f"  verification        ~ {len(recheck)} set to pending")

    # entities
    rows, fields = load("entities.csv")
    by_id = {r["entity_id"]: r for r in rows}
    for eid, changes in ENTITY_CHANGES.items():
        by_id[eid].update(changes)
    for eid, new_aliases in ALIASES.items():
        current = [a.strip() for a in by_id[eid]["also_known_as"].split(";") if a.strip()]
        current = ["FirstTrust[variant]" if a == "FirstTrust[typo]" else a for a in current]
        for alias in new_aliases:
            if alias not in current:
                current.append(alias)
        by_id[eid]["also_known_as"] = "; ".join(current)
    uk = by_id["uk-first-african-remittances-02722739"]
    if UK_NOTE_OLD in uk["notes"]:
        uk["notes"] = uk["notes"].replace(UK_NOTE_OLD, UK_NOTE_NEW)
    for new in NEW_ENTITIES:
        if new["entity_id"] not in by_id:
            rows.append({f: new.get(f, "") for f in fields})
    save("entities.csv", rows, fields)
    print("  entities            ~ corrected")

    # roles
    rows, fields = load("roles.csv")
    rows = [r for r in rows if r["role_id"] not in ROLES_REMOVED]
    for r in rows:
        r.update(ROLE_CHANGES.get(r["role_id"], {}))
    have = {r["role_id"] for r in rows}
    rows += [{f: n.get(f, "") for f in fields} for n in NEW_ROLES if n["role_id"] not in have]
    save("roles.csv", rows, fields)
    print("  roles               ~ corrected")

    # resolution review
    rows, fields = load("resolution_review.csv")
    for r in rows:
        r.update(RESOLUTION_CHANGES.get(r["candidate_id"], {}))
        if r["candidate_id"] == "RR007":
            for old, new in RR007_REPLACE:
                r["reason"] = r["reason"].replace(old, new)
    save("resolution_review.csv", rows, fields)
    print("  resolution_review   ~ corrected")

    # relationship types
    rows, fields = load("relationship_types.csv")
    for r in rows:
        r.update(REL_CHANGES.get(r["relationship"], {}))
    save("relationship_types.csv", rows, fields)
    print("  relationship_types  ~ corrected")

    # changelog
    rows, fields = load("changelog.csv")
    have = {r["change_id"] for r in rows}
    for cid, ctype, otype, oid, reason, sid in CHANGELOG:
        if cid not in have:
            rows.append({"change_id": cid, "version": VERSION, "change_date": TODAY,
                         "change_type": ctype, "object_type": otype, "object_id": oid,
                         "reason": reason, "source_id": sid})
    save("changelog.csv", rows, fields)
    print(f"  changelog           + up to {len(CHANGELOG)}")
    print("\nnow run: python run_all.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
