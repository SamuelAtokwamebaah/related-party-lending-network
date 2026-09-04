# related-party-lending-network

Modelling the insider relationships behind Ghana's 2019 savings & loans failures as a
network, built only from what the Bank of Ghana published.

> **Status: Phases 0–3 complete; evidence base verified at `v0.2`.** This repository is
> private until v1. All 39 edges have been checked against the Bank of Ghana notice by
> hand; the pass is recorded in `data/verification.csv` and versioned in
> `data/changelog.csv`. Nothing here is a finding about any institution or
> person: it is a record of what the source documents state, with every passage quoted
> and anchored to a line in the published notice.

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

It is the third repository in a deliberate arc:

1. `ghana-banking-collapse` — institutional failure analysis
2. `microfinance-fraud-detection` — transactional fraud detection
3. **`related-party-lending-network`** — insider network analysis

## Sourcing standard

- Primary sources only: Bank of Ghana notices, published court and regulatory documents,
  official registry data, and the verified dataset in `ghana-banking-collapse`.
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
The evidence base now holds 55 entities and 39 edges, of which 19 are documented with
both ends named and 18 name the relationship but not the counterparty.

Built independently from passages, it reproduces the published **17-of-23** finding: the
17 institutions carrying a value-extracting edge are exactly the 17 flagged for
related-party exposure in `ghana-banking-collapse`.

It also surfaced the constraint that shapes the whole project: **the documented graph
falls into 17 disconnected components**, largest 6 nodes, so whole-network centrality and
community detection are not yet meaningful and will not be presented as though they were.
Two genuine multi-entity structures do exist in the record and carry the analysis — the
Ideal Financial Holdings / FirsTrust / Ideal Finance cluster, and GN Savings and Loans
within the Groupe Nduom network.

The full assessment, including the recommended project mode and the open questions, is in
[docs/phase0/SOURCE-INVENTORY.md](docs/phase0/SOURCE-INVENTORY.md).

## Repository layout

```
data/         the evidence base: sources, entities, edges, evidence, roles,
              verification, changelog, entity-resolution review
data/raw/     extracted text of the source notice, as working copy
data/vendor/  the verified dataset carried over from ghana-banking-collapse
sources/      the source document as published
sql/          schema.sql - nine tables and two views
scripts/      phase0_extract_evidence.py    splits the notice, extracts evidence
              phase1_seed_from_phase0.py    one-off seed of the CSV model
              load.py                       validates, then builds the database
              build_review_pack.py          builds the verification sheets
              analyse_graph.py              builds the graph, computes the metrics
              phase2_report.py              writes the findings document
              build_site.py                 renders index.html
              site_template.py              the page shell and palette
docs/phase0/  SOURCE-INVENTORY.md   feasibility, mode decision, corrections
docs/phase1/  SCHEMA-PROPOSAL.md    the data model as built
docs/phase2/  FINDINGS.md           the analyses, with what they cannot show
              metrics.json          the same numbers, machine-readable
index.html    the network map, rendered from the database
docs/review/  one verification sheet per institution
```

## Reproducing

```
python run_all.py
```

Needs `networkx` (`pip install -r requirements.txt`); everything else is standard
library. Extracts the evidence from the notice, builds the database from the CSVs,
rebuilds the verification pack, runs the analyses, and renders the map. The database is a build artefact and is not
committed: if a figure is wrong, a CSV row is wrong.

The loader refuses to build if any validation rule fails, and names the row and the
reason. Two rules carry most of the weight: a quote must be verbatim **at the line its
anchor names**, and a named counterparty must actually be named in the passage cited for
its edge. Both exist because both failures happened.

## Verification

The evidence base was seeded by script and then checked by hand, edge by edge, against the
notice. `docs/review/` holds the pack that pass was worked from: one sheet per institution,
pairing each edge with the passage behind it and listing every passage in that section that
no edge cites — which is where a missed relationship would hide. Decisions are recorded in
`data/verification.csv` and the loader reports coverage on every build.

Two things remain deliberately open, and both are visible in the data rather than buried:

- `data/resolution_review.csv` holds three entity-resolution questions marked `undecided`.
  Nothing in hand settles them, and the tooling never merges entities on its own.
- Two edges are classed `inferred`. They rest on no source, carry no citation, and are
  excluded from every figure and from the map.

## Licence

MIT for the code. The source documents in `sources/` are public documents of the Bank of
Ghana and are reproduced for citation.
