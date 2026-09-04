# Phase 0 — source inventory and feasibility gate

Status: complete. Mode decided 4 September 2026 — see section 5.
Date: 4 September 2026.

This document answers one question: **what network can the sources in hand actually
support?** Nothing here is a finding about any institution or person. It is a count of
what the documents say, so that the graph design follows the evidence.

---

## 1. Sources in hand

| # | Source | Status | What it supports |
|---|--------|--------|------------------|
| S1 | Bank of Ghana, *Notice of revocation of licences of 23 savings and loans companies and finance houses*, 16 August 2019 | In hand, PDF + extracted text | The whole of the current graph. 9,645 words, 23 per-institution sections, each with a narrative history and a numbered list of the specific regulatory violations |
| S2 | Bank of Ghana, microfinance revocation notice, 31 May 2019 | In hand (`ghana-banking-collapse`) | Out of scope as nodes. Used once, for corroboration: one named related party of a scoped institution appears in this list as a revoked institution in its own right |
| S3 | Bank of Ghana, microcredit revocation notice, 31 May 2019 | In hand (`ghana-banking-collapse`) | Narrative context only |
| S4 | `ghana-banking-collapse` verified dataset (`savings_loans_verified.csv`) | In hand | Institution attributes: licence type, incorporation and licensing dates, insolvency date, net worth, CAR, and the coded failure causes including the related-party flag |
| S5 | Court and academic material in `act-930-resolution-timelines/sources/` | In hand, not yet mined | Unknown. The *Kohl v Consolidated Bank Ghana* judgments should be checked for named directors or shareholders of any scoped institution |

Everything in the graph today comes from **S1 alone**. That is a strength for
traceability — one document, one citation format, one publisher — and a limitation for
coverage, which section 4 sets out.

## 2. What S1 yields

Produced by `scripts/phase0_extract_evidence.py`, which splits the notice into its 23
sections and pulls every bullet carrying related-party, affiliate, ownership,
ownership-history, officer-role or exposure vocabulary. Output:
`docs/phase0/evidence-extract.md` (every matched bullet, quoted, anchored to a line
number) and `docs/phase0/source-inventory.csv` (one row per institution).

- 23 of 23 sections contain at least one matched bullet
- **69 matched bullets** in total
- 14 sections use the words "related party" or "related parties" explicitly
- 6 sections state an ownership history — an acquisition, a takeover or a renaming

Hand-curating those bullets into edges gives `docs/phase0/candidate-edges.csv`:

| | Count |
|---|---|
| Candidate edges | 41 |
| — documented, counterparty named | 22 |
| — documented, counterparty unnamed | 17 |
| — inferred, excluded from headline findings | 2 |
| Distinct nodes | 52 |
| Institutions carrying at least one related-party edge | **17 of 23** |

That 17 reproduces the headline finding already published in `ghana-banking-collapse`,
arrived at here by a different route — passage extraction rather than manual coding.
The two methods disagree on nothing.

One reconciliation detail worth keeping. A regex for "related part*" alone finds 14, not
17. The gap is institutions where the notice describes the same conduct in different
words — Global Access, where the institution "assumed the liability of a loan contracted
by the majority shareholder" and pays "high rent expenses" to that shareholder, never
uses the phrase "related party". The published flag is right and the narrow regex is
wrong. **Vocabulary, not conduct, is what varies across these 23 sections**, which is
the argument for extracting passages and reading them rather than counting keywords.

### Named entities the notice puts on the record

Eighteen entities other than the 23 institutions are named outright:

**Counterparties (11)** — AllTime Capital Limited; Ivory Finance Company Limited;
First African Remittances, UK; Ghana Growth Fund (Gold Coast Advisors); Gold Coast Fund
Management Limited (now Blackshield Capital Management); Ideal Capital Partners;
uniSecurities Limited; Liberty Asset Management; Liberty DMI Microfinance; Griffin
Financial Services; the Groupe Nduom network of businesses.

**Holding companies (3)** — Ideal Financial Holdings; Nordcom Africa Holdings Limited;
Hoda Group of Companies.

**Former names (4)** — Sterling Savings and Loans Limited; Apex Finance House Limited;
EZI Savings and Loans Limited; Kantamanto Savings and Loans Company Limited.

The holding companies matter most. They are the only entities in the source that sit
*above* an institution rather than beside it, and they are where person-level
directorship and shareholding would attach if a registry source is ever obtained.

### Documented but unnamed

Seventeen edges are real edges with an unlabelled endpoint. The notice states the
relationship, often the count, and sometimes the amount, but not the identity:

- First Allied — "the current accounts of eight (8) related companies linked to the
  major shareholder were overdrawn in excess of GHS 100.00 million"
- FirsTrust — "over exposed to six (6) of its related companies to the tune of
  GHS 17.93 million"
- Dream Finance — "over exposed to six (6) of its related companies"
- Crest — "exposures to its parent company **and a company in which the Chief Executive
  Officer is a director**"
- Global Access — a loan contracted by the majority shareholder, assumed by the
  institution and booked as equity capital, concealed in a suspense account

These are not stylized. A node labelled `UNNAMED eight related companies of First Allied`
asserts exactly what the Bank of Ghana asserted and no more. Treating them as a third
confidence class — `documented_unnamed`, alongside `documented` and `inferred` — keeps
them usable without overstating them.

## 3. The honest problem: the graph is fragmented

Union-find over the 39 non-inferred candidate edges:

- 52 nodes, 39 edges, **17 connected components**
- largest component: **7 nodes** — Ideal Financial Holdings, Ideal Finance Limited,
  FirsTrust Savings and Loans (formerly EZI), Ideal Capital Partners and two unnamed
  related-party groups
- second largest: 4 nodes
- adding both inferred edges changes nothing: still 17 components

**This matters more than any other line in this document.** Degree centrality,
betweenness centrality and community detection are all measures of position within a
connected structure. Run on 17 disconnected stars they will return near-zero betweenness
for almost every node and "communities" that are just the components. Reporting those
numbers as findings would be a metric dressed up as an insight, and any interviewer who
knows graphs would see it immediately.

What the source *does* support is real, and there is more of it than I expected:

1. **Two genuine multi-entity structures.**
   - *Ideal / FirsTrust.* Ideal Financial Holdings acquired EZI Savings and Loans in
     2014 and renamed it FirsTrust. Ideal Finance Limited then carried related-party
     exposure to FirsTrust and to Ideal Capital Partners totalling GHS 63.19 million.
     In June 2019 the two applied to merge; the Bank of Ghana declined on 25 July 2019
     because both were insolvent. A common owner, cross-lending between the two, and an
     attempted merger of the pair — all from one document. This is a closed loop, and
     the project's central claim in miniature.
   - *GN / Groupe Nduom.* GN Savings and Loans placed GHS 761.55 million with its sister
     companies Ghana Growth Fund (Gold Coast Advisors) and Gold Coast Fund Management
     Limited, now Blackshield Capital Management, both licensed by the Securities and
     Exchange Commission rather than the Bank of Ghana. The notice states plainly that
     the failure of those two to repay is what drove GN's insolvency.
2. **A typology of extraction mechanisms**, visible across all 23: lending to related
   companies; placing depositor funds with sister companies; transferring collateral to
   affiliates with no cash inflow; paying management fees and rent to shareholders;
   assuming a shareholder's personal liability and booking it as capital.
3. **Cross-source corroboration in one case.** Liberty DMI Microfinance, named as a
   related party of Midland, appears as entry 109 in the 31 May 2019 microfinance
   revocation list — a related party that was itself a failed licensed institution.

## 4. What would change the answer

Ranked by value against effort. Only the first three are realistic without money.

1. **SEC Ghana notice revoking fund-management licences (November 2019).** Public. Would
   give Gold Coast Fund Management / Blackshield, Liberty Asset Management, uniSecurities
   and possibly Ideal Capital Partners their own regulatory record. This is the single
   most likely source of *connectivity*, because the asset-management layer is where the
   same groups reappear across institutions.
2. **BoG notices of 1 August 2018 and 4 January 2019 (the universal banks).** Public.
   uniBank and GN Bank sit directly behind two of the scoped institutions. Admitting
   them requires a narrow amendment to the scope rule — see the question in section 6.
3. **UK Companies House** for First African Remittances, UK. Free, open, and it names
   directors. The one route in hand to a documented person-level node.
4. **Kohl v Consolidated Bank Ghana** and the other court material already downloaded.
   Cheap to check; unknown yield.
5. **Registrar-General company filings** for the three holding companies. This is what
   would actually build the director/shareholder layer the project was conceived around.
   Ghana's register is not freely searchable online and this realistically needs money
   and a physical search. Treat as out of reach and say so in the limitations section.
6. **Receiver's reports and full loan books.** Not public. Named in the limitations
   section as what access would enable, and nothing from the receivership engagement
   appears here.

## 5. Mode decision

**Decided 4 September 2026: hybrid, weighted heavily to real entities, with Phase 2
reframed.** The reasoning below is what the decision was taken on.

- Build the real-entity graph from the 22 documented edges. It is citable line by line
  and it already contains two structures worth walking a reader through.
- Keep the 17 `documented_unnamed` edges as first-class, rendered distinctly. They are
  the Bank of Ghana's own assertions with an unlabelled endpoint, not inventions.
- Keep `inferred` edges in the store, excluded from every headline figure and off by
  default in the visualization. There are two, both about common ownership implied by a
  shared name.
- **Do not claim a single connected insider network.** Replace the whole-graph centrality
  framing with: a typology of extraction mechanisms; per-institution structural
  attributes; two documented case networks in depth; and the 17-versus-6 comparison
  answered on structural attributes rather than on centrality.
- Compute the centrality and community measures anyway, and **publish the degenerate
  result as a documented non-result** — the same treatment the Benford test got in
  `microfinance-fraud-detection`. "The public record supports 17 components, so
  betweenness is uninformative" is a defensible sentence in an interview. A fabricated
  centrality ranking is not.
- Reserve the stylized reconstruction for a clearly-labelled appendix, if at all: one
  synthetic figure showing what the *same* structures look like when the counterparty
  identities are known, to make the point about what the public record withholds. It
  would illustrate, never evidence.

If sources 1–3 in section 4 land, the connectivity picture may change and Phase 2 can be
widened. That decision should be made against the evidence then, not assumed now.

## 6. Open questions before Phase 1

1. ~~**Scope amendment.**~~ **Decided 4 September 2026.** A non-S&L institution may enter
   as a node **only** where a scoped institution's own notice names it as a counterparty
   or a common owner — GN Bank and uniBank being the cases in view. Every such node is
   flagged as a documented scope exception in the methodology note and carries the
   citation that admitted it. The other 395 remain narrative context with no nodes.
2. **Sterling.** Commerz Savings and Loans is described as "formerly known as Sterling
   Savings and Loans Limited and part of Nordcom Africa Holdings Limited". Sterling
   Financial Services Limited is separately institution 21 on the same list. Same entity
   or different? Nothing in hand settles it, and the answer changes the graph. Needs a
   source before either treatment.
3. **Ideal reconciliation.** The notice gives Ideal Finance related-party exposure of
   GHS 63.19 million at one point and total related party loans of GHS 52.70 million at
   another. Different bases, probably; worth resolving before either number is published.
4. **Ideal Financial Holdings → Ideal Finance Limited.** Currently inferred from the
   shared name only. Confirmed or dropped, not assumed.
