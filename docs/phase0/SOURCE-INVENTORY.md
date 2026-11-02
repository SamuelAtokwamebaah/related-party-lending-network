# Phase 0: source inventory and feasibility gate

> **Historical document.** This is the feasibility assessment of 4 September 2026, kept as
> the record of how the project's mode was chosen. Counts and plans below are as they stood
> then. The current state is in the [README](../../README.md),
> [FINDINGS](../phase2/FINDINGS.md) and [LIMITATIONS](../LIMITATIONS.md). Since this was
> written, the SEC notice was admitted (v0.3), GN was taken out of the worked examples
> because its revocation is in live litigation, and a pre-release audit corrected the
> evidence base (v0.7). Where a statement below was later found to be wrong, it is marked
> in place.

Status: complete. Mode decided 4 September 2026; see section 5.
Date: 4 September 2026. Corrected the same day; see section 7.

This document answers one question: **what network can the sources in hand actually
support?** Nothing here is a finding about any institution or person. It is a count of
what the documents say, so that the graph design follows the evidence.

---

## 1. Sources in hand

| # | Source | Status | What it supports |
|---|--------|--------|------------------|
| S1 | Bank of Ghana, *Notice of revocation of licences of 23 savings and loans companies and finance houses*, 16 August 2019 | In hand, PDF + extracted text | The whole of the graph at Phase 0. 9,645 words, 23 per-institution sections, each with a narrative history and a numbered list of the specific regulatory violations |
| S2 | Bank of Ghana, microfinance revocation notice, 31 May 2019 | In hand (`ghana-banking-collapse`) | Out of scope as nodes. Used once, for corroboration: one named related party of a scoped institution appears in this list as a revoked institution in its own right |
| S3 | Bank of Ghana, microcredit revocation notice, 31 May 2019 | In hand (`ghana-banking-collapse`) | Narrative context only |
| S4 | `ghana-banking-collapse` verified dataset (`savings_loans_verified.csv`) | In hand | Institution attributes: licence type, incorporation and licensing dates, insolvency date, net worth, CAR, and the coded failure causes including the related-party flag |
| S5 | Court and academic material held by the author, not published | **Kohl mined 13 September 2026. Nothing admitted. GN Court of Appeal judgment (21 May 2026) mined the same day: one edge admitted, `E044`** | *Kohl v Consolidated Bank Ghana*, Court of Appeal, Civil Appeal No H1/95/2021, 28 November 2022, is a depositor of **Beige Bank**, a universal bank revoked on 1 August 2018, suing the bridge bank. The full text was searched against all 75 entities in `data/entities.csv`: **none is named**, and the one string match was the word "expressly". The only individuals it names are the parties, counsel, the bench and the Beige Bank receiver, none connected to a scoped institution. GhaLII carries it twice, as [2022] GHACA 61 and [2022] GHACA 156; both are the same judgment |

At the Phase 0 gate, everything in the graph came from **S1 alone**. That is a strength for
traceability (one document, one citation format, one publisher) and a limitation for
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
- 6 sections state an ownership history: an acquisition, a takeover or a renaming

Hand-curating those bullets into edges gives `docs/phase0/candidate-edges.csv`:

| | Count |
|---|---|
| Candidate edges | 43 |
| of which documented, counterparty named | 19 |
| of which documented, counterparty unnamed | 18 |
| of which inferred, excluded from headline findings | 2 |
| of which renamings, folded into aliases rather than kept as edges | 4 |
| Distinct nodes in the built graph | 50 |
| Institutions carrying at least one related-party edge | **17 of 23** |

That 17 reproduces the headline finding already published in `ghana-banking-collapse`,
arrived at here by a different route: passage extraction rather than manual coding.
The two methods disagree on nothing.

One reconciliation detail worth keeping. A regex for "related part*" alone finds 14, not
17. The gap is institutions where the notice describes the same conduct in different
words. Global Access, where the institution "assumed the liability of a loan contracted
by the majority shareholder" and pays "high rent expenses" to that shareholder, never
uses the phrase "related party". The published flag is right and the narrow regex is
wrong. **Vocabulary, not conduct, is what varies across these 23 sections**, which is
the argument for extracting passages and reading them rather than counting keywords.

### Named entities the notice puts on the record

Nineteen entities other than the 23 institutions are named outright:

**Counterparties (11)**: AllTime Capital Limited; Ivory Finance Company Limited;
First African Remittances, UK; Ghana Growth Fund (Gold Coast Advisors); Gold Coast Fund
Management Limited (now Blackshield Capital Management); Ideal Capital Partners;
uniSecurities Limited; Liberty Asset Management; Liberty DMI Microfinance; Griffin
Financial Services; International Business Solutions (USA).

**Holding companies (4)**: Groupe Nduom; Ideal Financial Holdings; Nordcom Africa
Holdings Limited; Hoda Group of Companies.

**Former names (4)**: Sterling Savings and Loans Limited; Apex Finance House Limited;
EZI Savings and Loans Limited; Kantamanto Savings and Loans Company Limited.

The holding companies matter most. They are the only entities in the source that sit
*above* an institution rather than beside it, and they are where person-level
directorship and shareholding would attach if a registry source is ever obtained.

### Documented but unnamed

Eighteen edges are real edges with an unlabelled endpoint. The notice states the
relationship, often the count, and sometimes the amount, but not the identity:

- First Allied: "the current accounts of eight (8) related companies linked to the
  major shareholder were overdrawn in excess of GHS 100.00 million"
- FirsTrust: "over exposed to six (6) of its related companies to the tune of
  GHS 17.93 million"
- Dream Finance: "over exposed to six (6) of its related companies"
- Crest: "exposures to its parent company **and a company in which the Chief Executive
  Officer is a director**"
- Global Access: a loan contracted by the majority shareholder, assumed by the
  institution and booked as equity capital, concealed in a suspense account

These are not stylised. A node labelled `UNNAMED eight related companies of First Allied`
asserts exactly what the Bank of Ghana asserted and no more. Treating them as a third
confidence class, `documented_unnamed`, alongside `documented` and `inferred`, keeps
them usable without overstating them.

## 3. The honest problem: the graph is fragmented

Union-find over the 37 non-inferred edges as built:

- 50 nodes, 37 edges, **17 connected components**
- two components of **6 nodes** each, and they are the two case networks:
  - Ideal Financial Holdings, Ideal Finance, FirsTrust (formerly EZI), Ideal Capital
    Partners and two unnamed related-party groups
  - Groupe Nduom, GN Savings and Loans, Ghana Growth Fund, Gold Coast Fund Management,
    International Business Solutions and one unnamed related-party group
- the remaining fifteen components hold 2 to 4 nodes each
- adding both inferred edges changes nothing: still 17 components

**This matters more than any other line in this document.** Degree centrality,
betweenness centrality and community detection are all measures of position within a
connected structure. Run on 17 disconnected stars they will return near-zero betweenness
for almost every node and "communities" that are just the components. Reporting those
numbers as findings would be a metric dressed up as an insight, and any reader who
knows graphs would see it immediately.

What the source *does* support is real, and there is more of it than expected:

1. **Two genuine multi-entity structures.**
   - *Ideal / FirsTrust.* Ideal Financial Holdings acquired EZI Savings and Loans in
     2014 and renamed it FirsTrust. Ideal Finance Limited then carried related-party
     exposure to FirsTrust and to Ideal Capital Partners totalling GHS 63.19 million.
     In June 2019 the two applied to merge; the Bank of Ghana declined their request of
     25 July 2019 because both were insolvent. A common owner, cross-lending between the two, and an
     attempted merger of the pair, all from one document. This is a closed loop, and
     *[Corrected at v0.7: the common owner of Ideal Finance is inferred from the name
     only (I001), and only one direction of exposure is documented. Phase 2 also found
     this cycle does not move value on every leg, because one leg is the merger
     application.]*
   - *GN / Groupe Nduom.* GN Savings and Loans placed GHS 761.55 million with its sister
     companies Ghana Growth Fund (Gold Coast Advisors) and Gold Coast Fund Management
     Limited, now Blackshield Capital Management, both licensed by the Securities and
     Exchange Commission rather than the Bank of Ghana. The notice states plainly that
     the failure of those two to repay is what drove GN's insolvency.
2. **A typology of related-party mechanisms**, visible across all 23: lending to related
   companies; placing depositor funds with sister companies; transferring collateral to
   affiliates with no cash inflow; paying management fees and rent to shareholders;
   assuming a loan contracted by the majority shareholder and booking it as capital.
3. **Cross-source corroboration in one case.** Liberty DMI Microfinance, named as a
   related party of Midland, appears as entry 109 in the 31 May 2019 microfinance
   revocation list: a related party that was itself a failed licensed institution.

## 4. What would change the answer

Ranked by value against effort. Only the first three are realistic without money.

1. **SEC Ghana notice revoking fund-management licences (November 2019).** Public. Would
   give Gold Coast Fund Management / Blackshield, Liberty Asset Management, uniSecurities
   and possibly Ideal Capital Partners their own regulatory record. This is the single
   most likely source of *connectivity*, because the asset-management layer is where the
   same groups reappear across institutions.
2. **BoG notices of 1 August 2018 and 4 January 2019 (the universal banks).** Public.
   uniBank and GN Bank sit directly behind two of the scoped institutions. Admitting
   them requires a narrow amendment to the scope rule; see the question in section 6.
3. **UK Companies House** for First African Remittances, UK. Free, open, and it names
   directors. The one route in hand to a documented person-level node.
4. **Kohl v Consolidated Bank Ghana** and the other court material already downloaded.
   Cheap to check; unknown yield.
5. **Registrar-General company filings** for the holding companies. This is what
   would actually build the director/shareholder layer the project was conceived around.
   Ghana's register is not freely searchable online and this realistically needs money
   and a physical search. Treat as out of reach and say so in the limitations section.
6. **Receiver's reports and full loan books.** Not public. Named in the limitations
   section as what access would enable, and nothing from the receivership engagement
   appears here.

## 5. Mode decision

**Decided 4 September 2026: hybrid, weighted heavily to real entities, with Phase 2
reframed.** The reasoning below is what the decision was taken on.

- Build the real-entity graph from the 22 documented edges (counted before the section 7
  corrections; 19 after). It is citable line by line
  and it already contains two structures worth walking a reader through.
- Keep the 17 (18 after section 7) `documented_unnamed` edges as first-class, rendered distinctly. They are
  the Bank of Ghana's own assertions with an unlabelled endpoint, not inventions.
- Keep `inferred` edges in the store, excluded from every headline figure and off by
  default in the visualisation. There are two, both about common ownership implied by a
  shared name.
- **Do not claim a single connected insider network.** Replace the whole-graph centrality
  framing with: a typology of related-party mechanisms; per-institution structural
  attributes; two documented case networks in depth; and the 17-versus-6 comparison
  answered on structural attributes rather than on centrality.
- Compute the centrality and community measures anyway, and **publish the degenerate
  result as a documented non-result**. "The public record supports 17 components, so
  betweenness is uninformative" is a defensible sentence. A fabricated
  centrality ranking is not.
- Reserve the stylised reconstruction for a clearly-labelled appendix, if at all: one
  synthetic figure showing what the *same* structures look like when the counterparty
  identities are known, to make the point about what the public record withholds. It
  would illustrate, never evidence.

If sources 1–3 in section 4 land, the connectivity picture may change and Phase 2 can be
widened. That decision should be made against the evidence then, not assumed now.

## 6. Open questions before Phase 1

1. ~~**Scope amendment.**~~ **Decided 4 September 2026.** A non-S&L institution may enter
   as a node **only** where a scoped institution's own notice names it as a counterparty
   or a common owner, GN Bank and uniBank being the cases in view. Every such node is
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

---

## 7. Corrections, 4 September 2026

Logged here and in `data/changelog.csv` because the affected artefacts were already
committed. Nothing published outside this repository relied on them.

1. **Every line anchor was wrong by up to 26 lines.** The extractor used Python's
   `str.splitlines()`, which breaks on form feeds as well as newlines. This notice
   carries 27 form feeds, one per page break, so anchors ran progressively ahead of the
   line a reader sees in `grep`, `sed` or an editor. Anchors now match. The quotes were
   never wrong, only the pointers to them, but an anchor nobody can follow is not a
   citation, so this was worth stopping for.
2. **Three GN edges pointed at the wrong paragraph.** E021, E022 and E023 were anchored
   to a generic passage rather than to the sister-company placements. Corrected to L798.
   The loader now carries a rule (12) that catches exactly this: a named counterparty
   must be named in the passage cited for it.
3. **Page-break truncation.** Quotes spanning a page break stopped mid-sentence and
   printed page numbers were being absorbed into them. The blocker now continues a
   passage across a page break when the sentence is unfinished, and treats a page number
   as furniture.
4. **One documented relationship had been missed.** The ownership pattern matched
   *owner* and *ownership* but not *owned*, hiding a passage that names **International
   Business Solutions**, a company the notice states is owned by Groupe Nduom and based
   in the USA, to which USD 62,255,516.93, GBP 718,528.59 and EUR 4,200 of depositors'
   funds were transferred without supporting documentation. This is now two edges, and
   it made Groupe Nduom a documented owner rather than only a network label.
5. **Amounts are not always in cedis.** Item 4 forced a schema change: `amount_ghs_m`
   became `amount_value` with `amount_currency` and `amount_unit` beside it.
