# Phase 1 — data model and CSV templates (proposal for review)

> **Historical document.** This is the data model as proposed and agreed at v0.1, kept as
> the record of the design decisions. The built schema has since grown: `sql/schema.sql`
> now holds fourteen tables and three views, a placement layer (`layer` on
> `relationship_types`), percentages as an amount unit, a `payments` category in place of
> `fee_extraction`, and a directional reading of `extracts_value` (LIMITATIONS section 8).
> Where this document and `sql/schema.sql` differ, the schema is current.

Status: **agreed 4 September 2026**, and built. The schema is in `sql/schema.sql`, the
loader in `scripts/load.py`, and the templates in `data/`. Section 5 records what was
decided and what is still open.
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

Everything else — centrality, communities, cycles — is Phase 2, and each measure will be
explained at the point it is used rather than in advance.

## 1. Design decisions taken from Phase 0

**A renaming is not a new node.** Crest was incorporated as Apex Finance House; FirsTrust
was EZI Savings and Loans; uniCredit was Kantamanto. Same legal person throughout. In the
Phase 0 candidate sheet these were modelled as edges to `former_name` nodes, which was wrong
— it would inflate the node count and invent structure. They become **aliases** of a
single entity instead. Only a transaction between two distinct legal persons is an edge.

**The notice misspells things, and the schema has to absorb that.** It writes "FirstTrust"
for FirsTrust and "Bank of Gnana" for Bank of Ghana; it also spells Groupe Nduom both
"Nduom" and "Ndoum". Aliases carry a `[typo]` type so the raw string that appears in a
quoted passage always resolves to the right entity without silently editing the quote.

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
| `amount_value` | numeric or blank |
| `amount_currency` | `GHS` / `USD` / `GBP` / `EUR`. Required whenever an amount is present |
| `amount_unit` | `million` / `units`. Required whenever an amount is present |
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
| `relationship` | `owns`, `acquired`, `part_of`, `controls`, `directs`, `lends_to`, `over_exposed_to`, `related_party_exposure_to`, `placed_funds_with`, `holds_deposits_in`, `overdrawn_current_accounts`, `transferred_collateral_to`, `transferred_funds_to`, `extended_overdraft_facilities_to`, `funded_projects_of`, `pays_management_fees_to`, `pays_rent_to`, `assumed_liability_of_loan_of`, `pre_financed_receivable_from`, `proposed_merger_with`, `succeeded` |
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
| `anchor` | `<source_id>:L<line>`. The line number as `grep`, `sed` or an editor counts it — see rule 11 |
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
11. Every quote in `evidence` is found verbatim **at the line its anchor names**
    (whitespace-normalised), not merely somewhere in the document
12. For an edge whose counterparty is a named company, that company's name — or one of
    its aliases — appears in the passage cited for that edge

Rules 11 and 12 are the ones worth the effort, and both were written the hard way.

Rule 11 originally checked only that a quote appeared *somewhere* in the source. That
passed while every anchor in the repository was wrong by up to 26 lines, because the
extractor used `str.splitlines()` and the notice carries 27 form feeds as page breaks.
The quotes were right; the pointers were not. Checking at the anchored line is what makes
an anchor followable.

Rule 12 catches the failure rule 11 cannot: an anchor that is verbatim, in range, and
still aimed at the wrong paragraph. Three GN edges were anchored to a generic passage
rather than to the sister-company placements. If a passage cited for "GN placed funds
with Gold Coast Fund Management" does not mention Gold Coast Fund Management, something
is wrong — and that is now a build failure rather than a reader's problem.

Both rules were checked by hand against a deliberately broken row: mis-anchoring a quote fires
rule 11, and repointing an edge at a real but unrelated passage fires rule 12.

## 5. Questions on this proposal

1. ~~**Six CSVs, or fewer?**~~ **Decided 4 September 2026: six.** Evidence keeps its own
   file. A passage supporting several edges is typed once, and the verbatim-match check
   (rule 11) has a single authoritative copy to verify against the source.
2. **`amount_basis`** — the four-value vocabulary held, but the source answered a
   different question first: **not every figure is in cedis.** The notice states one GN
   transfer as USD 62,255,516.93, GBP 718,528.59 and EUR 4,200. `amount_ghs_m` became
   `amount_value` with `amount_currency` and `amount_unit` beside it. Still open, and
   still needing your eye: (a) is there a fifth *basis* you have seen in receiver's
   reports, and (b) that GN transfer is **one relationship carrying three currencies**,
   which the current one-amount-per-edge model cannot hold. It sits in `amount_note` for
   now. If more multi-currency cases turn up as you compile, the right fix is a small
   `edge_amounts` child table — one edge, many amounts — rather than stretching the edge
   row. One case does not justify a seventh file; three or four would.
3. ~~**Should `roles` exist at all yet?**~~ **Kept**, on the migration argument above: it
   holds three placeholder rows today, but its existence means adding a registry source
   later is data entry rather than a schema change. Say if you would rather drop it.
4. ~~**Version stamping.**~~ **Decided 4 September 2026: per compilation session.** One
   bump per sitting — `v0.1`, `v0.2` — logged in `changelog.csv` with what changed and
   why.

## 6. Alias types

`also_known_as` entries carry a bracketed type so a raw string in a quoted passage always
resolves to the right entity without editing the quote:

| marker | meaning | example |
|---|---|---|
| `[former]` | earlier name of the same legal person | `EZI Savings and Loans Limited[former]` on FirsTrust |
| `[later]` | name adopted after the conduct described | `Blackshield Capital Management[later]` on Gold Coast Fund Management |
| `[typo]` | the source's own misspelling | `FirstTrust[typo]` on FirsTrust |
| `[variant]` | punctuation or abbreviation difference | `uniCredit Savings & Loans Ltd.[variant]` |

Canonical name is the name the entity held **at the time of the conduct described**, so
Gold Coast Fund Management Limited is canonical and Blackshield is the alias. Reversing
that would make the citation read oddly against the notice.
