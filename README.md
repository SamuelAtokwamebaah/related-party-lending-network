# related-party-lending-network

Modelling the insider relationships behind Ghana's 2019 savings & loans failures as a
network, built only from what the regulators published.

> **Status: complete at `v0.5.1`.** All 69 edges have been checked by hand against the
> source that supports them, and the decisions are recorded in `data/verification.csv` and
> versioned in `data/changelog.csv`. Nothing here is a finding about any institution or
> person: it is a record of what two regulators published, with every passage quoted and
> anchored to a line in the source document.

**New here?** Three ways in, in ascending order of detail:

| | |
|---|---|
| [`index.html`](index.html) | the map. Every connection is hoverable and shows the passage behind it |
| [docs/LIMITATIONS.md](docs/LIMITATIONS.md) | **what this cannot show, and why.** Read it before the findings, not after |
| [docs/phase2/FINDINGS.md](docs/phase2/FINDINGS.md) | the analyses in full, including the ones that returned nothing |

---

## Why this project

`ghana-banking-collapse` established that **related-party lending appears in 17 of the 23
savings & loans companies and finance houses** whose licences the Bank of Ghana revoked
on 16 August 2019. That is a count. It says how often insider lending appears; it says
nothing about how it was structured, or whether the same people and companies sit behind
more than one failure.

This project asks the structural question. Institutions, their owners, their holding
companies and their connected borrowers are modelled as a graph, so that the shape of the
extraction is visible rather than merely tallied.

It is the third repository in a deliberate arc, and each one answers a different kind of
question about the same collapse:

| | repository | question | method |
|---|---|---|---|
| 1 | `ghana-banking-collapse` | *which* institutions failed, and why | institutional failure analysis over a verified dataset |
| 2 | `microfinance-fraud-detection` | what fraud looks like at **transaction** level | detection on transactional data |
| 3 | **`related-party-lending-network`** | how insiders were **structurally** connected | network analysis over a cited evidence base |

The third is the one that could most easily have been faked, and that is the point of how
it is built. A network diagram is persuasive whether or not the relationships in it are
real. So every node and every edge here carries a source document and a line number, the
loader refuses to build if a quote is not verbatim at the line its citation names, and the
analyses that returned nothing are published alongside the ones that did.

## Sourcing standard

- Primary sources only: Bank of Ghana and Securities and Exchange Commission notices,
  published court and regulatory documents, official registry data, and the verified
  dataset in `ghana-banking-collapse`.
- Every node and every edge carries a source document and a line-level anchor.
- Each edge carries a confidence class:
  - `documented` — the source names both ends of the relationship
  - `documented_unnamed` — the source states the relationship, and often the count and
    the amount, but not the counterparty's identity
  - `inferred` — not stated in any source in hand. Excluded from every headline figure
    and off by default in the visualization.
- The graph reports what the documents state. It makes no allegation beyond the public
  record, and takes no position on any live proceeding.

## Where things stand

Phase 0 read the 16 August 2019 notice end to end and inventoried what it can support.
The evidence base now holds 74 entities and 69 edges, of which 49 are documented with
both ends named, 18 name the relationship but not the counterparty, and 2 are inferred
and excluded from every figure. Of those, **54 edges form the related-party graph** and
13 sit in a separate placement layer described below.

The 17 institutions carrying a value-extracting edge are exactly the 17 flagged for
related-party exposure in `ghana-banking-collapse` — but that agreement is a **consistency
check, not a confirmation**. Both sides are readings of the same Bank of Ghana notice, so
the separation was close to guaranteed. It shows the extraction pipeline neither dropped
an institution nor invented one. It is not a second source corroborating the first, and
this repository does not present it as one.

It also surfaced the constraint that shapes the whole project: **the documented graph
falls into 17 disconnected components**, largest 10 nodes, so whole-network centrality and
community detection are not meaningful and will not be presented as though they were. A
modularity of 0.89 is high here because the graph is fragmented, not because structure
was found.

Adding a second regulator changed two of those results, which is the argument for the
sourcing standard rather than against it:

- **One entity now connects two of the 23.** Ideal Capital Partners holds related-party
  positions in both Ideal Finance and FirsTrust. Phase 2 reported, from the Bank of Ghana
  notice alone, that no entity did. That was stated as a property of the document — *the
  notice does not name one* — rather than of the world, which is why the finding could be
  updated instead of retracted.
- **The one closed funding loop appears in neither notice alone.** The Bank of Ghana
  records Midland as over-exposed to Liberty Asset Management; the Securities and Exchange
  Commission records Liberty placing 9.45% of its funds with Midland. Each held the other,
  and value moves along both arrows. Four cycles exist and exactly one qualifies: the
  other three carry a merger application or an acquisition on some leg, which is
  structure, not money. It is called a *funding* loop rather than an extraction loop on
  purpose — value leaves Midland to a related party and that party's client money funds
  Midland. Whether either side ended better off is not something these documents say.

The three worked examples are the uniCredit / uniSecurities / Hoda component, the Ideal
Financial Holdings cluster, and Midland / Liberty. GN Savings and Loans is **not** among
them: on 21 May 2026 the Court of Appeal quashed the revocation of its licence and the
Bank of Ghana's appeal to the Supreme Court is pending. Its edges remain in the data,
still attributed to the Bank of Ghana, which did publish those statements, but the
repository takes no position on a live proceeding and keeps contested institutions out of
its worked examples.

The full assessment, including the recommended project mode and the open questions, is in
[docs/phase0/SOURCE-INVENTORY.md](docs/phase0/SOURCE-INVENTORY.md).

## The placement layer, and what it costs to keep it separate

The Commission's notice describes a second kind of relationship the Bank of Ghana's does
not: a fund manager placing client money in one of the 23, with **no related-party claim
attached**. Value moves; no insider relationship is alleged. There are 13 such edges from
7 fund managers, reaching 8 of the 23.

They are held in a separate layer — `layer = 'placement'` in `relationship_types`,
filtered out of `v_institution_profile`, excluded from every figure in the related-party
analysis, and shown on the page in a table rather than in the diagrams.

The reason is a number rather than a principle. Five of the seven fund managers name more
than one of the 23. Admitting these as ordinary edges would take the graph from **17
components, largest 10** to **12 components, largest 26** — one structure holding most of
the graph. That structure is real, and it is not an insider network: it is a set of
institutions that share a fund manager who placed client money in both. It would be the
most impressive version of this project and the least true one.

One of the eight institutions the placement layer reaches is **Commerz**, which the Bank
of Ghana did *not* flag for related-party exposure — and a separate fund manager, Nordea
Capital, is recorded as placing 50% of its funds under management with Commerz *as a
related party*. The clean 17-against-6 split is a property of the Bank of Ghana notice,
not of the record as a whole.

## The search that found something and changed nothing

`docs/LIMITATIONS.md` named UK Companies House as the one route in reach to a documented
person-level node. It has now been searched, and the result is worth reading as a method
rather than as a finding.

The register holds **FIRST AFRICAN REMITTANCES LIMITED (02722739)**, incorporated in 1992
as First African Forex Bureau Limited, in financial intermediation, which applied to strike
itself off on 30 May 2019 and was dissolved on 22 October 2019 — two months after the Bank
of Ghana revoked First African Savings and Loans' licence, citing GHS 5.40m its UK
affiliate had not reimbursed. Two directors serving at dissolution, both recorded as
Ghanaian nationals resident in Accra. One person with significant control.

Name, jurisdiction, business, director residence and timing all converge. **Nothing states
the identification**, so it is `RR007`, undecided, and no edge depends on it. The company
sits in the evidence base and not in the graph: 63 nodes and 54 edges, exactly as before.

The register also names the individuals. They are **not reproduced here**. No regulator has
named any individual in connection with this failure, and the identification is open —
naming them would assert by juxtaposition a connection no document makes. Counts,
nationalities and the filing sequence are recorded; names are not.

**On provenance.** The register's summary pages publish no archived document, so what
could be transcribed from them was, at first, all there was — and a quote checked against a
transcription is only checked against the transcription. That has been fixed where it
matters. The Registrar's own notices are downloaded and vendored in `sources/`: the first
Gazette notice, the striking-off suspension, and the dissolution. They are one-page scans
with no text layer, so rule 11 cannot machine-check them, but a reader can check a few
lines against a one-page PDF in the repository in about a minute.

That upgrade also turned an inference into a quotation. The suspension of the strike-off
had been read from the filing sequence; the notice states it outright — *"suspended as an
objection has been received by the Registrar"*. The Registrar does not say who objected.

The register-summary transcription now supports only what nothing else does: the registered
and previous names, incorporation, office, business classification, and the officer and
control counts.

## Repository layout

```
data/         the evidence base: sources, entities, edges, evidence, roles,
              verification, changelog, entity-resolution review
data/raw/     extracted text of the source notices, as working copies
data/vendor/  the verified dataset carried over from ghana-banking-collapse
sources/      the source documents as published
sql/          schema.sql - fourteen tables and three views
scripts/      phase0_extract_evidence.py    splits the notice, extracts evidence
              phase1_seed_from_phase0.py    one-off seed of the CSV model
              load.py                       validates, then builds the database
              build_review_pack.py          verification sheets, BoG notice
              build_sec_review.py           verification sheets, SEC notice
              analyse_graph.py              builds the graph, computes the metrics
              phase2_report.py              writes the findings document
              build_site.py                 renders index.html
              site_template.py              the page shell and palette
              integrate_sec_notice.py       one-off, idempotent: admits the SEC notice
              integrate_placement_layer.py  one-off: the rest of that notice, and
                                            the placement layer
docs/LIMITATIONS.md  what this cannot show, and why - read first
docs/phase0/  SOURCE-INVENTORY.md   feasibility, mode decision, corrections
docs/phase1/  SCHEMA-PROPOSAL.md    the data model as built
docs/phase2/  FINDINGS.md           the analyses, with what they cannot show
              metrics.json          the same numbers, machine-readable
index.html    the network map, rendered from the database
docs/review/  one verification sheet per institution (Bank of Ghana notice)
docs/review/sec/  the SEC notice: sections with edges, and coverage of all 53
```

## Reproducing

```
python run_all.py
```

Needs `networkx` (`pip install -r requirements.txt`); everything else is standard
library. Extracts the evidence from the Bank of Ghana notice, builds the database from
the CSVs, rebuilds the verification pack, runs the analyses, and renders the map. The
database is a build artefact and is not committed: if a figure is wrong, a CSV row is
wrong.

The loader refuses to build if any validation rule fails, and names the row and the
reason. Two rules carry most of the weight: a quote must be verbatim **at the line its
anchor names**, and a named counterparty must actually be named in the passage cited for
its edge. Both exist because both failures happened.

## Verification

The evidence base was seeded by script and then checked by hand, edge by edge, against the
source. [docs/review/](docs/review/) holds the pack that pass was worked from: one sheet
per institution for the Bank of Ghana notice, and in [docs/review/sec/](docs/review/sec/)
one sheet per cited section of the Commission's notice plus a coverage sheet listing all
53 of its sections.

What makes the pack worth having is what it lists *besides* the citations: every passage
in the same section that no edge cites, and every section of the Commission's notice from
which no edge was drawn. That is where a missed relationship hides, and it has caught one
— the Commission's notice was under-read at v0.3, and eight sections naming one of the 23
went unnoticed until every section was listed rather than only the cited ones.

Decisions are recorded in `data/verification.csv` and the loader reports coverage on every
build. A figure on the page or in the findings is marked provisional automatically for as
long as any edge behind it is unchecked.

All 69 edges now carry a decision. Two things remain deliberately open, and both are
visible in the data rather than buried:

- `data/resolution_review.csv` holds five entity-resolution questions marked `undecided`.
  Nothing in hand settles them, and the tooling never merges entities on its own. The one
  that would change the graph is whether Hoda Holdings Ltd, named by the Commission as a
  related party of uniSecurities, is the Hoda Group of Companies that the Bank of Ghana
  says acquired uniCredit. A sixth was closed at v0.4: the Commission calls Legacy Capital
  Savings a related party of Legacy Fund Management, so that pair no longer rests on a
  shared name. A seventh was opened at v0.5 by the Companies House search — see below.
- Two edges are classed `inferred`. They rest on no source, carry no citation, and are
  excluded from every figure and from the map.

## Licence

MIT for the code. The source documents in `sources/` are public documents of the Bank of
Ghana and of the Securities and Exchange Commission, and are reproduced for citation.
