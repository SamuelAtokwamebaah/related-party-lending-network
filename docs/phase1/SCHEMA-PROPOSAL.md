# Phase 1 — data model and CSV templates (proposal for review)

Status: **proposal**. No loader code is written until this is agreed.
Date: 4 September 2026.

Built to the mode decided at the Phase 0 gate: a real-entity spine, with
`documented_unnamed` edges as first-class citizens and `inferred` edges quarantined.

---

## 0. The one piece of graph theory needed to read this

A graph is nodes joined by edges. This one is a **directed multigraph**:

- **Directed** — the edge has a direction, and it matters. "Institution lends to related
  company" and "shareholder owns institution" point opposite ways, and value flows along
  the arrow. Direction is what will later let us ask whether ownership and lending fold
  back on each other.
- **Multigraph** — more than one edge is allowed between the same pair of nodes. Ideal
  Finance both lends to FirsTrust *and* applied to merge with it. Those are two different
  relationships and collapsing them into one "connection" would throw away the thing that
  makes the pair interesting.

Everything else — centrality, communities, cycles — is Phase 2, and I will explain each
measure at the point it is used rather than in advance.

## 1. Design decisions taken from Phase 0

**A renaming is not a new node.** Crest was incorporated as Apex Finance House; FirsTrust
was EZI Savings and Loans; uniCredit was Kantamanto. Same legal person throughout. In the
Phase 0 candidate sheet I modelled these as edges to `former_name` nodes, which was wrong
— it would inflate the node count and invent structure. They become **aliases** of a
single entity instead. Only a transaction between two distinct legal persons is an edge.

**The notice misspells things, and the schema has to absorb that.** It writes "FirstTrust"
for FirsTrust and "Bank of Gnana" for Bank of Ghana. Aliases carry a `typo_in_source`
type so the raw string that appears in a quoted passage always resolves to the right
entity without silently editing the quote.

**Placeholders are typed, counted, and never merged.** `UNNAMED eight related companies of
First Allied` is one node standing for eight companies, with `member_count = 8`. It is
never merged with any other placeholder, because nothing in the record says two
institutions' unnamed related parties are the same companies. That restraint is the whole
point of the `documented_unnamed` class.

**Amounts need a basis, not just a number.** The notice gives GHS 100.00 million as a
floor ("in excess of"), GHS 761.55 million as a combined total across two counterparties,
and 319% as a ratio with no amount at all. Storing a bare number would silently turn three
different kinds of statement into one. Hence `amount_basis`.

## 2. Tables

Nine tables in SQLite, built from six CSVs you populate plus two the tooling maintains.

### `sources` — one row per document
| column | notes |
|---|---|
| `source_id` | slug, e.g. `bog-2019-08-16-savings-loans-revocation` |
| `title`, `publisher`, `published_date` | as printed on the document |
| `doc_type` | `revocation_notice` / `judgment` / `registry_extract` / `dataset` / `regulator_notice` |
| `url`, `local_path`, `retrieved_date` | provenance |
| `notes` | e.g. how the text was extracted |

### `entities` — one row per node
| column | notes |
|---|---|
| `entity_id` | stable slug, e.g. `inst-firstrust`, `hold-ideal-financial-holdings`, `ph-first-allied-8` |
| `canonical_name` | the name used in output |
| `entity_type` | `institution` / `holding_company` / `corporate_entity` / `person` / `placeholder_group` |
| `also_known_as` | `;`-separated aliases, each optionally suffixed `[typo]` or `[former]` |
| `scope_class` | `core_23` / `scope_exception` / `counterparty` / `placeholder` |
| `regulator` | `BoG` / `SEC` / `none` / `unknown` — Gold Coast and uniSecurities were SEC-licensed, and that cross-regulator hop is part of the story |
| `jurisdiction` | `GH` / `UK` / `unknown` |
| `member_count` | integer, placeholders only. 8 for First Allied, 6 for FirsTrust and Dream, blank where the notice gives no count |
| `is_named` | 0 for placeholders, 1 otherwise |
| `admitted_by_edge_id` | required when `scope_class = scope_exception`; the edge whose citation admitted this node under the Phase 0 scope rule |
| `evidence_anchors` | `;`-separated, into `evidence` |
| `notes` | |

### `edges` — one row per relationship
| column | notes |
|---|---|
| `edge_id` | stable, e.g. `E018`. Never reused, never renumbered |
| `source_entity_id`, `target_entity_id` | direction is source → target, value flowing along the arrow where the relationship is a transfer |
| `relationship` | from the controlled vocabulary in `relationship_types` |
| `amount_ghs_m` | numeric or blank |
| `amount_basis` | `exact` / `floor` / `combined_total` / `ratio_only` / `none`. Required whenever an amount is present |
| `amount_note` | e.g. "combined GHS 63.19m across E024 and E025" |
| `as_at_date` | the date the source attaches to the figure, not the date of the notice |
| `confidence` | `documented` / `documented_unnamed` / `inferred` |
| `evidence_anchors` | `;`-separated. Required unless `confidence = inferred`, which must have none |
| `review_note` | mandatory free text for `inferred`; optional otherwise |
| `version_added`, `version_removed` | evidence-base version stamps |

### `relationship_types` — the controlled vocabulary
| column | notes |
|---|---|
| `relationship` | `owns`, `acquired`, `part_of`, `controls`, `directs`, `lends_to`, `over_exposed_to`, `related_party_exposure_to`, `placed_funds_with`, `holds_deposits_in`, `overdrawn_current_accounts`, `transferred_collateral_to`, `pays_management_fees_to`, `pays_rent_to`, `assumed_liability_of_loan_of`, `pre_financed_receivable_from`, `proposed_merger_with`, `succeeded` |
| `category` | `ownership` / `lending` / `placement` / `fee_extraction` / `governance` / `corporate_action` |
| `extracts_value` | 0/1 — does this relationship move value *out* of the institution? |
| `description` | one plain sentence |

`extracts_value` is the field that earns its keep in Phase 2. It separates edges that
drain the institution (lending to an affiliate, paying rent to a shareholder, assuming a
shareholder's loan) from edges that merely describe structure (a holding company owning
an institution). "Which institutions had the most value-extracting edges, and to whom"
is answerable without any centrality measure at all.

### `evidence` — one row per quoted passage
| column | notes |
|---|---|
| `anchor` | `bog-2019-08-16:L592`. Source slug plus line number in the working text |
| `source_id` | FK to `sources` |
| `quote` | **verbatim**, including the source's own typos |
| `page` | printed page number where visible, for citing the PDF rather than the text file |
| `extracted_date` | |

One passage often supports several edges — Crest's L443 supports two — and one edge can
rest on several passages. The `;`-separated `evidence_anchors` column is exploded into a
proper many-to-many join table by the loader, so the CSV stays typeable and the database
stays normalised.

### `roles` — person or entity holding a role at an institution
| column | notes |
|---|---|
| `role_id`, `entity_id`, `institution_id` | |
| `role_type` | `director` / `shareholder` / `majority_shareholder` / `board_chairman` / `ceo` / `officer` |
| `start_date`, `end_date` | usually blank from the notice |
| `confidence`, `evidence_anchors` | |

Nearly empty today — three placeholder people, from Crest, First Allied and Global
Access. It exists because it is exactly where registry or Companies House data would land,
and building it now means adding that source later is a data-entry job rather than a
schema migration.

### `institution_attributes` — joined from `ghana-banking-collapse`
Licence type, incorporation and licensing dates, insolvency date, net worth, CAR, and the
coded failure causes, keyed on `entity_id`. Loaded from `savings_loans_verified.csv`, not
retyped. This is what makes the Phase 2 comparative question (the 17 against the other 6)
answerable at all.

### `resolution_review` — maintained by the tooling, decided by you
| column | notes |
|---|---|
| `candidate_id`, `name_a`, `name_b`, `entity_id_a`, `entity_id_b` | |
| `similarity` | string-similarity score that raised it |
| `reason` | why it was flagged |
| `decision` | `same` / `different` / `undecided` — defaults to `undecided` |
| `decided_date`, `decision_note` | |

The loader flags candidates and **never merges anything on its own**. Two live cases
already: Sterling Savings and Loans (Commerz's former name) against Sterling Financial
Services (institution 21), and whether Ivory Finance Company is a predecessor alias of CDH
or a distinct entity it acquired. Both currently `undecided`, and both stay out of the
graph's headline structure until decided against a source.

### `changelog` — the versioned evidence base
| column | notes |
|---|---|
| `change_id`, `version`, `change_date` | version as `v0.1`, `v0.2`, … |
| `change_type` | `add` / `correct` / `remove` |
| `object_type`, `object_id` | `edge` / `entity` / `role` / `alias` |
| `reason` | why, in a sentence |
| `source_id` | the document that prompted it, where there is one |

Every published figure names the version it was computed from. When a finding changes,
the reason it changed is on the record — the same discipline as withdrawing the 180-day
claim in the Act 930 work.

## 3. CSVs you populate

Six, in `data/`:

```
sources.csv       one row per document
entities.csv      one row per node
edges.csv         one row per relationship
evidence.csv      one row per quoted passage
roles.csv         one row per role held
changelog.csv     one row per change to the evidence base
```

`relationship_types.csv` ships with the repo as a fixed vocabulary.
`resolution_review.csv` is written by the loader for you to decide on.

**Suggested working order per institution:** read the section → paste each relevant
passage into `evidence.csv` with its anchor → add any new entity to `entities.csv` → add
the edges to `edges.csv` referencing those anchors → log the batch in `changelog.csv`.
Evidence before edges, so nothing can be asserted without a quote sitting behind it.

The Phase 0 `candidate-edges.csv` is the seed for `edges.csv` — 41 rows already drafted
with anchors, minus the four renaming rows which become aliases instead.

## 4. What the loader will enforce

Refuse to build the database, with a named row and reason, if any of these fail:

1. Every `entity_id` in `edges` and `roles` exists in `entities`
2. Every anchor in `evidence_anchors` exists in `evidence`
3. Every `relationship` is in `relationship_types`
4. `confidence` is one of the three permitted values
5. `documented` and `documented_unnamed` edges have at least one evidence anchor
6. `inferred` edges have **no** evidence anchor and **do** have a `review_note`
7. `amount_basis` is present and non-`none` whenever `amount_ghs_m` is
8. `entity_type = placeholder_group` implies `is_named = 0`
9. `scope_class = scope_exception` implies a populated `admitted_by_edge_id`
10. No duplicate `edge_id` or `entity_id`
11. Every quote in `evidence` is found verbatim in the source text at the anchored line
    (whitespace-normalised) — this is the check that makes the citations mean something,
    and it will catch a mistyped anchor immediately

Rule 11 is the one worth the effort. Without it, an anchor is a claim; with it, an anchor
is verified.

## 5. Questions on this proposal

1. **Six CSVs, or fewer?** Evidence could be folded into `edges.csv` as a quote column,
   dropping a file, at the cost of retyping a passage that supports several edges and
   losing the guarantee that both copies match. I lean to keeping it separate, but you are
   the one typing.
2. **`amount_basis` — is the four-value vocabulary right** against what you have seen in
   receiver's reports, or is there a fifth kind of figure it misses?
3. **Should `roles` exist at all yet**, given it will hold three placeholder rows? I say
   yes, for the migration reason above, but it is dead weight until a registry source
   lands.
4. **Version stamping** — one version per compilation session, or per institution
   completed? Per session is less bookkeeping; per institution is finer-grained
   traceability.
