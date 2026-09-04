# related-party-lending-network

Modelling the insider relationships behind Ghana's 2019 savings & loans failures as a
network, built only from what the Bank of Ghana published.

> **Status: Phase 0 complete.** This repository is private while the evidence base is
> assembled. Nothing here is a finding about any institution or person — Phase 0 is a
> count of what the source documents state, and every passage used is quoted and
> anchored to a line number in the published notice.

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

Phase 0 read the 16 August 2019 notice end to end and inventoried what it can support:
41 candidate edges over 52 nodes, of which 22 are documented with both ends named. The
extraction reproduces the published 17-of-23 finding by an independent route.

It also surfaced the constraint that shapes the whole project: **the documented graph
falls into 17 disconnected components**, so whole-network centrality and community
detection are not yet meaningful and will not be presented as though they were. Two
genuine multi-entity structures do exist in the public record and carry the analysis.

The full assessment, including the recommended project mode and the open questions, is in
[docs/phase0/SOURCE-INVENTORY.md](docs/phase0/SOURCE-INVENTORY.md).

## Repository layout

```
data/raw/     extracted text of the source notice, as working copy
sources/      the source document as published
scripts/      phase0_extract_evidence.py — splits the notice, extracts evidence
docs/phase0/  SOURCE-INVENTORY.md   the feasibility assessment and mode decision
              evidence-extract.md   every matched bullet, quoted and anchored
              source-inventory.csv  one row per institution
              candidate-edges.csv   hand-curated candidate edges for review
```

## Reproducing Phase 0

```
python scripts/phase0_extract_evidence.py
```

Standard library only. It rewrites `docs/phase0/evidence-extract.md` and
`docs/phase0/source-inventory.csv` from the source text.

## Licence

MIT for the code. The source documents in `sources/` are public documents of the Bank of
Ghana and are reproduced for citation.
