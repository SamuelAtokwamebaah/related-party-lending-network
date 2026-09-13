# Verification sheet: Court of Appeal, GN Savings and Loans, 21 May 2026

Suit No. H1/71/2026. Working text: `data/raw/ca-2026-05-21-gn-savings-appeal.txt`.
Integrated by `scripts/integrate_gn_judgment.py`.

The original is a 31-page certified true copy, a scan with no text layer. It is **not** in
this repository because it names individuals; it is held in
`act-930-resolution-timelines/sources/ca-2026-05-21-gn-savings-appeal.pdf`.

Rule 11 checks each quote against the transcription. Only a person can check the
transcription against the scan, and that is what this sheet is for.

---

## Part 1: the transcription against the scan

Open the PDF at the printed page and compare word for word.

| Line | Printed page | Passage starts | Used for |
|---|---|---|---|
| L35 | 1 | `3. GN SAVINGS AND LOANS LTD ......3RD RESPONDENT` | E044: fixes "3rd respondent" as GN |
| L39 | 1 to 2 | `The 1st applicant/appellant is a shareholder of the 2nd and 3rd...` | E044 review note: membership "until" receivership |
| L43 | 13 | `"Besides, while the applicants' case is to the effect...` | Declined, see Part 3 |
| L47 | 14 | `It is not disputed that the 3rd respondent is a member of Groupe Ndoum...` | E044: the relationship |
| L51 | 14 to 15 | `Exhibit PNK 3 is an "Assignment of Receivables"...` | Declined, see Part 3 |

---

## Part 2: the edge

### E044: GN Savings and Loans Ltd. to Groupe Nduom

| | |
|---|---|
| relationship | `part_of` |
| confidence | `documented` |
| anchors | `ca-2026-05-21-gn-savings-appeal:L35`, `ca-2026-05-21-gn-savings-appeal:L47` |
| current decision | confirmed, 13 September 2026 |

> 3. GN SAVINGS AND LOANS LTD ......3RD RESPONDENT

> It is not disputed that the 3rd respondent is a member of Groupe Ndoum (3rd appellant), but since the Audit Reports are about the entire Groupe Ndoum and there is no indication anywhere therein that all or some of the IPCs are directly to the benefit of the 3rd respondent, we do not see how that can form a basis of saying that the figures therein form part of the assets of 3rd respondent; as debts owed it by the Government of Ghana.

Does the passage support the relationship, the direction, and `documented`? Record the
decision against `E044` in `data/verification.csv`.

---

## Part 3: read and deliberately not admitted

Recorded in `data/changelog.csv` as `C027`.

| Passage | Why not |
|---|---|
| Coconut Grove Beach Resort and Conference Centre Ltd, shareholder of GN and member of Groupe Nduom (L31, L39) | The scope rule of 4 September 2026 admits a non-S&L node only where a scoped institution's own notice names it. Not widened for one leaf on a component that is already connected |
| Gold Coast Advisors, "an affiliate company of the 3rd respondent" (L43) | The trial judge summarising the applicants' case, not a finding of the Court of Appeal. The Bank of Ghana already calls it a sister company (E022) |
| Assignment of receivables, GH¢629,091,335, to GN (L51) | Evidence on the value of GN's assets, the question under appeal. It also runs into GN, not out |
| "formerly known as Ghana Growth Fund Company Ltd" (L51) | Corroborates an alias `corp-ghana-growth-fund` already carries. No row needed |
| Capital deficit of GH¢344.46m in the Bank of Ghana's affidavit, against GHS 683.66m in its notice | A solvency figure. Recorded, not reconciled |
| Individuals named as shareholder and chairman, and the supervisor's recommendations about them | The person layer stays empty. See `docs/LIMITATIONS.md` section 1 |
