"""
v0.5 - the Companies House record for FIRST AFRICAN REMITTANCES LIMITED.

docs/LIMITATIONS.md named UK Companies House as the one route in reach to a
documented person-level node, and said it had not been searched. It has now.

What the search found: FIRST AFRICAN REMITTANCES LIMITED, company number
02722739, incorporated 12 June 1992 as FIRST AFRICAN FOREX BUREAU LIMITED,
registered in London, financial intermediation, dissolved by voluntary strike-off
on 22 October 2019. Two directors serving at dissolution, both recorded as
Ghanaian nationals resident in Ghana; one person with significant control.

Two decisions were taken before any of it was written down.

The identification is NOT treated as established. The Bank of Ghana names "First
African Remittances, UK" as an affiliate of First African Savings and Loans. The
register holds a company of that name, in that jurisdiction, in that business,
with Ghanaian directors resident in Accra, dissolved two months after the licence
was revoked. That is a strong convergence and it is still not a document saying
the two are the same. It enters as RR007, undecided, and no edge depends on it.
The company is therefore an isolated node: it is in the evidence base and not in
the graph.

The individuals are NOT reproduced. The register names them; no regulator has
named any of them in connection with this failure. Putting them in a repository
about a banking collapse, on the strength of an identification this project
itself marks undecided, would assert by juxtaposition a connection that no
document makes. Counts and nationalities are recorded; names are not. The person
layer stays honestly empty rather than being filled with people no document
accuses of anything.

Usage:  python scripts/integrate_companies_house.py
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
VERSION = "v0.5"
TODAY = "2026-09-04"
CH = "companies-house-02722739-first-african-remittances"


def read_source():
    text = (DATA / "raw" / f"{CH}.txt").read_text(encoding="utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def quote(first, last):
    lines = read_source()
    return " ".join(" ".join(lines[first - 1:last]).split())


def load(name):
    with (DATA / name).open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader), reader.fieldnames


def save(name, rows, fields):
    with (DATA / name).open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def append(name, key, new_rows):
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


SOURCES = [{
    "source_id": CH,
    "title": "Companies House register extract, FIRST AFRICAN REMITTANCES LIMITED (02722739)",
    "publisher": "Companies House, United Kingdom",
    "published_date": "",
    "doc_type": "registry_extract",
    "url": "https://find-and-update.company-information.service.gov.uk/company/02722739",
    "local_path": f"data/raw/{CH}.txt",
    "retrieved_date": TODAY,
    "notes": ("Transcribed from the register's web pages on the retrieval date, not "
              "downloaded: the register publishes no archived document for a company "
              "record and its API needs a key. A quote checked against data/raw/ is "
              "therefore checked against the transcription, not against the register. "
              "This is weaker provenance than every other source here. Officer and "
              "person-with-significant-control names are on the public register and "
              "are deliberately not transcribed."),
}]

ENTITIES = [{
    "entity_id": "uk-first-african-remittances-02722739",
    "canonical_name": "First African Remittances Limited (UK 02722739)",
    "entity_type": "corporate_entity",
    "also_known_as": "First African Forex Bureau Limited[former]",
    "scope_class": "counterparty",
    "regulator": "none",
    "jurisdiction": "UK",
    "member_count": "",
    "is_named": "1",
    "admitted_by_edge_id": "",
    "evidence_anchors": f"{CH}:L30; {CH}:L42; {CH}:L69",
    "notes": ("The company of this name on the UK register. Held apart from "
              "'First African Remittances, UK', the affiliate the Bank of Ghana "
              "names, because no document states they are the same: see RR007. "
              "No edge depends on it, so it is in the evidence base and not in "
              "the graph."),
    "status_note": "",
}]

EVIDENCE = [
    (30, 30),   # registered name
    (42, 42),   # previous name
    (46, 46),   # dissolution
    (52, 54),   # directors: counts and nationality, no names
    (59, 61),   # PSC: count, no name
    (69, 69),   # strike-off application
    (73, 73),   # strike-off suspended
]

RESOLUTION = [{
    "candidate_id": "RR007",
    "name_a": "First African Remittances, UK",
    "entity_id_a": "corp-first-african-remittances",
    "name_b": "First African Remittances Limited (UK 02722739)",
    "entity_id_b": "uk-first-african-remittances-02722739",
    "similarity": "0.85",
    "reason": ("The Bank of Ghana names 'First African Remittances, UK' as an affiliate "
               "of First African Savings and Loans. The UK register holds a company of "
               "that name (02722739), incorporated 1992 as First African Forex Bureau "
               "Limited, in financial intermediation, with two directors recorded as "
               "Ghanaian nationals resident in Accra, which applied to strike itself off "
               "on 30 May 2019 and was dissolved on 22 October 2019 - two months after "
               "the licence was revoked over GHS 5.40m the affiliate had not reimbursed."),
    "decision": "undecided",
    "decided_date": "",
    "decision_note": ("Strong convergence on name, jurisdiction, business, director "
                      "residence and timing. No document states the identification, and "
                      "this project has never resolved an identity on convergence alone. "
                      "Deciding it 'same' would connect the register record - including "
                      "named individuals no regulator has named - to a failed institution."),
}]

CHANGELOG = [
    ("C016", "add", "source", CH,
     "Companies House register extract for FIRST AFRICAN REMITTANCES LIMITED "
     "(02722739). docs/LIMITATIONS.md named this search as the one route in reach to a "
     "documented person-level node and recorded that it had not been done. It has now "
     "been done, and the result is recorded whichever way the identification goes.", CH),
    ("C017", "add", "entity", "uk-first-african-remittances-02722739",
     "The registered UK company admitted as its own entity rather than merged with the "
     "affiliate the Bank of Ghana names. It carries no edge and does not enter the "
     "graph; it exists so the search is on the record and nobody repeats it.", CH),
    ("C018", "add", "resolution", "RR007",
     "Whether company 02722739 is the affiliate the Bank of Ghana describes. Undecided. "
     "The convergence is strong - name, jurisdiction, business, Ghanaian directors "
     "resident in Accra, dissolution two months after the revocation - and convergence "
     "is not a document. Resolving it would connect named individuals to a bank failure "
     "that no regulator has connected them to.", CH),
    ("C019", "correct", "policy", "person-layer",
     "The person layer stays empty by decision, not by absence of data. The register "
     "names two serving directors, several resigned officers and one person with "
     "significant control. Those names are public and are not reproduced here: no "
     "regulator has named any individual in connection with this failure, and the "
     "identification linking the company to it is undecided. Counts, nationalities and "
     "the filing sequence are recorded; names are not.", CH),
]


def main():
    print(f"integrating the Companies House record at {VERSION}\n")

    print(f"  sources             + {append('sources.csv', 'source_id', SOURCES)}")

    ev = [{"anchor": f"{CH}:L{a}", "source_id": CH, "quote": quote(a, b),
           "page": "", "extracted_date": TODAY} for a, b in EVIDENCE]
    print(f"  evidence            + {append('evidence.csv', 'anchor', ev)}")

    print(f"  entities            + {append('entities.csv', 'entity_id', ENTITIES)}")
    print(f"  resolution          + {append('resolution_review.csv', 'candidate_id', RESOLUTION)}")

    cl = [{"change_id": c[0], "version": VERSION, "change_date": TODAY,
           "change_type": c[1], "object_type": c[2], "object_id": c[3],
           "reason": c[4], "source_id": c[5]} for c in CHANGELOG]
    print(f"  changelog           + {append('changelog.csv', 'change_id', cl)}")

    print("\n  edges added: 0. That is the point: the record is cited and the")
    print("  identification is open, so nothing in the graph moves.")
    print("\nnow run: python run_all.py")


if __name__ == "__main__":
    sys.exit(main())
