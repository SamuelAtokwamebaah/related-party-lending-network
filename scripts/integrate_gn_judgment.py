"""
v0.6 - the Court of Appeal judgment on GN Savings and Loans, read from the document.

Until now GN's status rested on a press explainer, and the source row said the
judgment had not been obtained. A certified true copy is now in hand: Suit No.
H1/71/2026, 21 May 2026, 31 pages, a scan with no text layer.

What it adds is one relationship. The court states, as undisputed, that GN is a
member of Groupe Nduom (page 14), and its introduction dates the membership as
lasting until the receivership (pages 1 to 2). The Bank of Ghana notice places GN's
related parties in "the Groupe Ndoum network of businesses" but never states GN's
own membership in terms. That becomes E044, the first edge in this repository
attributed to a court rather than a regulator.

Four decisions were taken before anything was written down.

The original is NOT vendored. It names individuals - the first appellant, the bench,
counsel, the receiver - and the Companies House filings that name directors were
withheld for the same reason. The PDF is held with the Kohl judgments in
act-930-resolution-timelines/sources/. The transcription in data/raw/ carries the
passages used, with printed page numbers, and replaces individuals' names with a
bracketed description.

The person layer stays empty. The judgment names GN's chairman and a shareholder, so
"no document makes the connection" no longer holds for this institution. But GN is
the one institution where the latest decision found the revocation unjustified, and
adding its chairman to a graph of insider relationships behind the failures would
imply a conclusion that decision cuts against.

Nothing on solvency enters. The appeal is live and the Supreme Court has stayed the
judgment. The assignment of receivables to GN, and the trial judge's description of
Gold Coast Advisors as an affiliate, are transcribed and not admitted.

Coconut Grove Beach Resort is NOT admitted as a node. The court names it as a
shareholder of GN and a member of Groupe Nduom, but the scope rule decided on
4 September 2026 admits a non-S&L node only where a scoped institution's own notice
names it. One leaf on a component that is already connected does not justify
widening that rule to court documents.

Usage:  python scripts/integrate_gn_judgment.py
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
VERSION = "v0.6"
TODAY = "2026-09-13"
CA = "ca-2026-05-21-gn-savings-appeal"

STAY = ("https://www.citinewsroom.com/2026/07/"
        "supreme-court-halts-reinstatement-of-gn-savings-licence/")


def read_source():
    text = (DATA / "raw" / f"{CA}.txt").read_text(encoding="utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def line(n, expect):
    text = read_source()[n - 1]
    assert text.startswith(expect), f"L{n} does not start {expect!r}: {text[:60]!r}"
    return text.strip()


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


def update(name, key, value, changes):
    rows, fields = load(name)
    hits = [r for r in rows if r[key] == value]
    assert len(hits) == 1, f"{name}: expected one row {key}={value}, found {len(hits)}"
    changed = any(hits[0][f] != v for f, v in changes.items())
    hits[0].update(changes)
    if changed:
        save(name, rows, fields)
    return int(changed)


SOURCE = {
    "title": ("Judgment, Suit No. H1/71/2026, three applicants/appellants v Bank of Ghana, "
              "Attorney-General and GN Savings and Loans Ltd"),
    "publisher": "Court of Appeal (Civil Division), Accra",
    "published_date": "2026-05-21",
    "doc_type": "judgment",
    "url": "",
    "local_path": f"data/raw/{CA}.txt",
    "retrieved_date": TODAY,
    "notes": (
        "Certified true copy stamped by the Registrar of the Court of Appeal, 31 pages, a scan "
        "with no text layer. The transcription carries only the passages used or deliberately "
        "declined, each with its printed page number, and was checked by eye against the scan; "
        "rule 11 checks quotes against the transcription, not the scan. The original is not "
        "vendored because it names individuals; it is held with the Kohl judgments in "
        "act-930-resolution-timelines/sources/. The Supreme Court stayed execution of this "
        f"judgment on 14 July 2026 pending the Bank of Ghana's appeal ({STAY}); that is press "
        "reporting and no document is in hand. Replaces a press explainer recorded on "
        "4 September 2026. Cited for relationships only, never for solvency or valuation."),
}

EVIDENCE = [
    (35, "3. GN SAVINGS AND LOANS LTD", "1"),
    (47, "It is not disputed that the 3rd respondent", "14"),
]

EDGE = {
    "edge_id": "E044",
    "source_entity_id": "inst-gn",
    "target_entity_id": "hold-groupe-nduom",
    "relationship": "part_of",
    "confidence": "documented",
    "evidence_anchors": f"{CA}:L35;{CA}:L47",
    "review_note": (
        "Stated as undisputed by the Court of Appeal (p.14). The judgment writes '3rd "
        "respondent'; the title of the suit (p.1) fixes that as GN. Its introduction (pp.1-2, "
        "transcription L39) says the membership lasted until the receivership. The Bank of Ghana notice (L798) "
        "places GN's related parties in the Groupe Nduom network but never states GN's own "
        "membership. First edge attributed to a court"),
    "version_added": VERSION,
}

STATUS_NOTE = (
    "On 21 May 2026 the Court of Appeal (Suit No. H1/71/2026) quashed the Bank of Ghana's "
    "16 August 2019 revocation of this institution's licence and ordered it restored, read "
    f"from a certified true copy transcribed in data/raw/{CA}.txt. The Supreme Court stayed "
    "execution of that judgment on 14 July 2026 pending the Bank of Ghana's appeal (press "
    "reporting; no document in hand), so the licence has not been restored and the matter is "
    "live. E021 to E023 and E042 remain as published by the Bank of Ghana and are attributed "
    "to it. E044, membership of Groupe Nduom, is attributed to the Court of Appeal and "
    "carries no position on solvency.")

CHANGELOG = [
    ("C024", "correct", "source", CA,
     "The press explainer is replaced by the judgment itself. A certified true copy of the Court "
     "of Appeal judgment of 21 May 2026 is now in hand and transcribed, page-anchored, in "
     "data/raw/. The original is not vendored because it names individuals, consistent with the "
     "Companies House filings at v0.5. The Supreme Court stay of 14 July 2026, which this "
     "repository previously described only as a pending appeal, is now recorded, from press "
     "reporting. Closes LIMITATIONS section 13, route 5.", CA),
    ("C025", "add", "edge", "E044",
     "GN Savings and Loans is a member of Groupe Nduom. The Court of Appeal states it as "
     "undisputed (p.14) and dates it as lasting until the receivership (pp.1-2). The Bank of "
     "Ghana notice implied it and never stated it. Both nodes were already in one component, "
     "so the component count is unchanged. The judgment also confirms, from a second source, "
     "that Gold Coast Advisors was formerly Ghana Growth Fund Company Ltd, an alias "
     "corp-ghana-growth-fund already carries.", CA),
    ("C026", "correct", "entity", "inst-gn",
     "Status note rewritten: the Court of Appeal outcome is cited from the judgment, the "
     "Supreme Court stay is added and attributed to press reporting, and the attribution of "
     "each GN edge is stated.", CA),
    ("C027", "add", "note", "gn-judgment-not-admitted",
     "Read in the judgment and deliberately not admitted. (1) Coconut Grove Beach Resort and "
     "Conference Centre Ltd, named by the court as a shareholder of GN and a member of Groupe "
     "Nduom: the scope rule of 4 September 2026 admits a non-S&L node only where a scoped "
     "institution's own notice names it, and it is not widened for one leaf. (2) Gold Coast "
     "Advisors as 'an affiliate company of the 3rd respondent' (p.13): the trial judge "
     "summarising the applicants' case, not a Court of Appeal finding. (3) An assignment of "
     "receivables of GHS 629,091,335 to GN (pp.14-15): evidence on the value of GN's assets, "
     "the question under appeal. (4) A capital deficit of GHS 344.46 million in the Bank of "
     "Ghana's affidavit, against GHS 683.66 million in its notice: a solvency figure, recorded "
     "and not reconciled. (5) Individuals named as chairman and shareholder: the person layer "
     "stays empty. GN is the one institution where the latest decision found the revocation "
     "unjustified, and adding its chairman to a graph of insider relationships behind the "
     "failures would imply a conclusion that decision cuts against.", CA),
]


def main():
    print(f"integrating the GN Court of Appeal judgment at {VERSION}\n")

    print(f"  sources             ~ {update('sources.csv', 'source_id', CA, SOURCE)}")

    ev = [{"anchor": f"{CA}:L{n}", "source_id": CA, "quote": line(n, expect),
           "page": page, "extracted_date": TODAY} for n, expect, page in EVIDENCE]
    print(f"  evidence            + {append('evidence.csv', 'anchor', ev)}")

    print(f"  edges               + {append('edges.csv', 'edge_id', [EDGE])}")

    # New edges enter unverified. The decision is Samuel's, made against the scan.
    ver = [{"edge_id": "E044", "decision": "pending", "note": "", "verified_date": "",
            "verified_by": ""}]
    print(f"  verification        + {append('verification.csv', 'edge_id', ver)}")

    print(f"  entities            ~ "
          f"{update('entities.csv', 'entity_id', 'inst-gn', {'status_note': STATUS_NOTE})}")

    cl = [{"change_id": c[0], "version": VERSION, "change_date": TODAY,
           "change_type": c[1], "object_type": c[2], "object_id": c[3],
           "reason": c[4], "source_id": c[5]} for c in CHANGELOG]
    print(f"  changelog           + {append('changelog.csv', 'change_id', cl)}")

    print("\n  nodes added: 0. edges added: 1. components: unchanged.")
    print("\nnow run: python run_all.py")


if __name__ == "__main__":
    sys.exit(main())
