-- Schema for the related-party lending evidence base.
--
-- The database is a build artefact. It is dropped and rebuilt from the CSVs in
-- data/ on every run, and it is never edited directly - if a figure is wrong,
-- the CSV row is wrong, and the changelog records why it changed.
--
-- Foreign keys are declared and enforced (PRAGMA foreign_keys = ON in the
-- loader). CHECK constraints carry the rules that are cheap to state in SQL;
-- the rules that need to read the source text live in scripts/load.py.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS verification;
DROP TABLE IF EXISTS edge_evidence;
DROP TABLE IF EXISTS role_evidence;
DROP TABLE IF EXISTS entity_evidence;
DROP TABLE IF EXISTS edges;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS aliases;
DROP TABLE IF EXISTS institution_attributes;
DROP TABLE IF EXISTS entities;
DROP TABLE IF EXISTS evidence;
DROP TABLE IF EXISTS relationship_types;
DROP TABLE IF EXISTS resolution_review;
DROP TABLE IF EXISTS changelog;
DROP TABLE IF EXISTS sources;

-- ---------------------------------------------------------------------------
-- Provenance
-- ---------------------------------------------------------------------------

CREATE TABLE sources (
    source_id       TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    publisher       TEXT NOT NULL,
    published_date  TEXT,
    doc_type        TEXT NOT NULL CHECK (doc_type IN (
                        'revocation_notice', 'regulator_notice', 'judgment',
                        'registry_extract', 'dataset')),
    url             TEXT,
    local_path      TEXT,
    retrieved_date  TEXT,
    notes           TEXT
);

-- One row per quoted passage. The quote is verbatim, including the source's
-- own typos, and the loader refuses to build unless it is found at the
-- anchored line in the source text.
CREATE TABLE evidence (
    anchor          TEXT PRIMARY KEY,      -- 'bog-2019-08-16-...:L592'
    source_id       TEXT NOT NULL REFERENCES sources(source_id),
    quote           TEXT NOT NULL,
    page            TEXT,
    extracted_date  TEXT
);

-- ---------------------------------------------------------------------------
-- Nodes
-- ---------------------------------------------------------------------------

CREATE TABLE entities (
    entity_id           TEXT PRIMARY KEY,
    canonical_name      TEXT NOT NULL,
    entity_type         TEXT NOT NULL CHECK (entity_type IN (
                            'institution', 'holding_company', 'corporate_entity',
                            'person', 'placeholder_group')),
    scope_class         TEXT NOT NULL CHECK (scope_class IN (
                            'core_23', 'scope_exception', 'counterparty', 'placeholder')),
    regulator           TEXT CHECK (regulator IN ('BoG', 'SEC', 'none', 'unknown')),
    jurisdiction        TEXT,
    member_count        INTEGER,
    is_named            INTEGER NOT NULL CHECK (is_named IN (0, 1)),
    -- Required when the node entered under the Phase 0 scope exception: the
    -- edge whose citation admitted a non-S&L institution to the graph.
    admitted_by_edge_id TEXT,
    notes               TEXT,
    -- A placeholder is by definition not named, and vice versa.
    CHECK ((entity_type = 'placeholder_group') <= (is_named = 0)),
    CHECK ((scope_class = 'placeholder') = (is_named = 0)),
    CHECK ((scope_class = 'scope_exception') <= (admitted_by_edge_id IS NOT NULL))
);

-- Exploded from the ';'-separated also_known_as column, so a raw string in a
-- quoted passage resolves to the right entity without editing the quote.
CREATE TABLE aliases (
    entity_id   TEXT NOT NULL REFERENCES entities(entity_id),
    alias_name  TEXT NOT NULL,
    alias_type  TEXT NOT NULL CHECK (alias_type IN ('former', 'later', 'typo', 'variant')),
    PRIMARY KEY (entity_id, alias_name)
);

-- Institution attributes carried over from ghana-banking-collapse rather than
-- retyped. This is what makes the 17-against-6 comparison answerable.
CREATE TABLE institution_attributes (
    entity_id                 TEXT PRIMARY KEY REFERENCES entities(entity_id),
    licence_type              TEXT,
    incorporated              TEXT,
    licensed                  TEXT,
    insolvent_since           TEXT,
    net_worth_ghs_m           REAL,
    car_pct                   REAL,
    related_party_exposure    INTEGER,
    governance_failure        INTEGER,
    liquidity_failure         INTEGER,
    misreporting              INTEGER,
    high_npl                  INTEGER,
    cause_count               INTEGER
);

-- ---------------------------------------------------------------------------
-- Edges
-- ---------------------------------------------------------------------------

-- The controlled vocabulary. extracts_value marks relationships that move value
-- out of the institution, as against those that only describe structure.
CREATE TABLE relationship_types (
    relationship    TEXT PRIMARY KEY,
    category        TEXT NOT NULL CHECK (category IN (
                        'ownership', 'lending', 'placement', 'fee_extraction',
                        'governance', 'corporate_action')),
    extracts_value  INTEGER NOT NULL CHECK (extracts_value IN (0, 1)),
    description     TEXT NOT NULL
);

-- A directed multigraph: more than one edge is allowed between the same pair,
-- because lending to an entity and applying to merge with it are different
-- facts and collapsing them would lose the thing that makes the pair notable.
CREATE TABLE edges (
    edge_id           TEXT PRIMARY KEY,
    source_entity_id  TEXT NOT NULL REFERENCES entities(entity_id),
    target_entity_id  TEXT NOT NULL REFERENCES entities(entity_id),
    relationship      TEXT NOT NULL REFERENCES relationship_types(relationship),
    -- Amounts are not always in cedis: the notice states one transfer in USD,
    -- GBP and EUR. Value, currency and unit are kept apart so a figure cannot
    -- be added to another that means something different.
    amount_value      REAL,
    amount_currency   TEXT CHECK (amount_currency IN ('GHS', 'USD', 'GBP', 'EUR')),
    amount_unit       TEXT CHECK (amount_unit IN ('million', 'units')),
    amount_basis      TEXT CHECK (amount_basis IN (
                          'exact', 'floor', 'combined_total', 'ratio_only', 'none')),
    amount_note       TEXT,
    as_at_date        TEXT,
    confidence        TEXT NOT NULL CHECK (confidence IN (
                          'documented', 'documented_unnamed', 'inferred')),
    review_note       TEXT,
    version_added     TEXT NOT NULL,
    version_removed   TEXT,
    -- An amount without a basis is three different kinds of statement
    -- flattened into one number.
    CHECK (amount_value IS NULL OR (amount_basis IS NOT NULL AND amount_basis <> 'none'
                                    AND amount_currency IS NOT NULL AND amount_unit IS NOT NULL)),
    -- An inferred edge rests on no source and must say why it is held at all.
    CHECK (confidence <> 'inferred' OR (review_note IS NOT NULL AND review_note <> ''))
);

-- Whether a human has checked a seeded row against the notice. Seeded rows are
-- a first pass; nothing here is verified until it carries a decision.
CREATE TABLE verification (
    edge_id        TEXT PRIMARY KEY REFERENCES edges(edge_id),
    decision       TEXT NOT NULL CHECK (decision IN (
                       'pending', 'confirmed', 'corrected', 'rejected')),
    note           TEXT,
    verified_date  TEXT,
    verified_by    TEXT
);

CREATE TABLE edge_evidence (
    edge_id  TEXT NOT NULL REFERENCES edges(edge_id),
    anchor   TEXT NOT NULL REFERENCES evidence(anchor),
    PRIMARY KEY (edge_id, anchor)
);

-- ---------------------------------------------------------------------------
-- Roles
-- ---------------------------------------------------------------------------

-- Nearly empty today: three placeholder people. It exists so that adding a
-- registry or Companies House source later is data entry, not a migration.
CREATE TABLE roles (
    role_id         TEXT PRIMARY KEY,
    entity_id       TEXT NOT NULL REFERENCES entities(entity_id),
    institution_id  TEXT NOT NULL REFERENCES entities(entity_id),
    role_type       TEXT NOT NULL CHECK (role_type IN (
                        'director', 'shareholder', 'majority_shareholder',
                        'board_chairman', 'ceo', 'officer')),
    start_date      TEXT,
    end_date        TEXT,
    confidence      TEXT NOT NULL CHECK (confidence IN (
                        'documented', 'documented_unnamed', 'inferred')),
    notes           TEXT
);

CREATE TABLE role_evidence (
    role_id  TEXT NOT NULL REFERENCES roles(role_id),
    anchor   TEXT NOT NULL REFERENCES evidence(anchor),
    PRIMARY KEY (role_id, anchor)
);

CREATE TABLE entity_evidence (
    entity_id  TEXT NOT NULL REFERENCES entities(entity_id),
    anchor     TEXT NOT NULL REFERENCES evidence(anchor),
    PRIMARY KEY (entity_id, anchor)
);

-- ---------------------------------------------------------------------------
-- Review and audit
-- ---------------------------------------------------------------------------

-- The loader flags near-duplicate names here and never merges anything itself.
CREATE TABLE resolution_review (
    candidate_id   TEXT PRIMARY KEY,
    name_a         TEXT NOT NULL,
    entity_id_a    TEXT,
    name_b         TEXT NOT NULL,
    entity_id_b    TEXT,
    similarity     REAL,
    reason         TEXT,
    decision       TEXT NOT NULL CHECK (decision IN ('same', 'different', 'undecided')),
    decided_date   TEXT,
    decision_note  TEXT
);

-- Every published figure names the version it was computed from, and every
-- change to the evidence base records why.
CREATE TABLE changelog (
    change_id    TEXT PRIMARY KEY,
    version      TEXT NOT NULL,
    change_date  TEXT NOT NULL,
    change_type  TEXT NOT NULL CHECK (change_type IN ('add', 'correct', 'remove')),
    object_type  TEXT NOT NULL,
    object_id    TEXT,
    reason       TEXT NOT NULL,
    source_id    TEXT REFERENCES sources(source_id)
);

-- ---------------------------------------------------------------------------
-- Convenience views
-- ---------------------------------------------------------------------------

-- Edges with both endpoints named and the quote that supports each one. This is
-- what the visualization's click-through reads.
CREATE VIEW v_edges_cited AS
SELECT
    e.edge_id,
    se.canonical_name AS source_name,
    se.entity_type    AS source_type,
    te.canonical_name AS target_name,
    te.entity_type    AS target_type,
    e.relationship,
    rt.category,
    rt.extracts_value,
    e.amount_value,
    e.amount_currency,
    e.amount_unit,
    e.amount_basis,
    e.confidence,
    COALESCE(v.decision, 'pending') AS verification,
    ev.anchor,
    ev.quote
FROM edges e
JOIN entities se ON se.entity_id = e.source_entity_id
JOIN entities te ON te.entity_id = e.target_entity_id
JOIN relationship_types rt ON rt.relationship = e.relationship
LEFT JOIN verification v ON v.edge_id = e.edge_id
LEFT JOIN edge_evidence ee ON ee.edge_id = e.edge_id
LEFT JOIN evidence ev ON ev.anchor = ee.anchor
WHERE e.version_removed IS NULL OR e.version_removed = '';

-- Per-institution extraction profile: how many value-extracting edges, to how
-- many distinct counterparties, and how much of it is named.
CREATE VIEW v_institution_profile AS
SELECT
    en.entity_id,
    en.canonical_name,
    ia.related_party_exposure,
    COUNT(*)                                            AS edges_out,
    SUM(rt.extracts_value)                              AS value_extracting_edges,
    COUNT(DISTINCT e.target_entity_id)                  AS distinct_counterparties,
    SUM(CASE WHEN e.confidence = 'documented' THEN 1 ELSE 0 END)        AS named_edges,
    SUM(CASE WHEN e.confidence = 'documented_unnamed' THEN 1 ELSE 0 END) AS unnamed_edges,
    -- Only value-extracting edges are summed. amount_basis records how a
    -- figure was stated, not what it measures, so without this filter a
    -- projected merger cash injection lands in the same total as a
    -- related-party exposure.
    SUM(CASE WHEN e.amount_basis = 'exact' AND e.amount_currency = 'GHS'
                  AND rt.extracts_value = 1
             THEN e.amount_value END)                                   AS extracted_ghs_m
FROM entities en
JOIN edges e ON e.source_entity_id = en.entity_id
JOIN relationship_types rt ON rt.relationship = e.relationship
LEFT JOIN institution_attributes ia ON ia.entity_id = en.entity_id
WHERE en.scope_class = 'core_23'
  AND e.confidence <> 'inferred'
GROUP BY en.entity_id, en.canonical_name, ia.related_party_exposure;
