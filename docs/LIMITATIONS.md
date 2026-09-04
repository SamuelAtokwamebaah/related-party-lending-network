# Limitations

What this project cannot show, and why. Written to be read on its own, before or instead
of the findings.

Figures are as at evidence base `v0.4`. `docs/phase2/metrics.json` is authoritative if
this document and the data ever disagree; every claim below is checkable against
`data/` and the two notices in `sources/`.

---

## 1. It names no individuals, and it was supposed to

The project was conceived to model insider relationships: who owned the institutions that
failed, who sat on their boards, and whether the same people appear behind more than one
failure. **The evidence base contains no named person.** The two `person` nodes in the
graph are both placeholders — *"UNNAMED major shareholder of First Allied"* and *"UNNAMED
majority shareholder of Global Access"* — because that is exactly as far as the Bank of
Ghana's notice goes.

This is the single largest gap, and no amount of analysis closes it. What the graph
actually models is **relationships between companies**: institutions, their holding
companies, their group affiliates and their fund managers. That is a real structure and it
is worth reading. It is not the ownership network the project set out to build, and the
network diagrams should not be read as though a person sits behind each node.

Building the person layer needs the Registrar-General's company filings. Ghana's register
is not freely searchable online; the realistic route is a paid physical search in Accra.

**UK Companies House has now been searched, and the layer is still empty — by decision.**
The register holds FIRST AFRICAN REMITTANCES LIMITED (02722739), incorporated 12 June 1992
as First African Forex Bureau Limited, in financial intermediation, dissolved by voluntary
strike-off on 22 October 2019. It names two directors serving at dissolution, both
recorded as Ghanaian nationals resident in Accra, and one person with significant control.

Those names are public and are not reproduced in this repository. Two reasons, and both
have to hold before a name goes in:

- **No regulator has named any individual in connection with this failure.** The Bank of
  Ghana notice names the company, not its officers.
- **The identification is undecided.** Nothing in hand states that company 02722739 *is*
  the "First African Remittances, UK" the Bank of Ghana describes, and this project has
  never resolved an identity on convergence alone. It is recorded as `RR007`.

Naming three private individuals in a repository about a banking collapse, on the strength
of an identification the project itself marks open, would assert by juxtaposition a
connection no document makes. The counts, nationalities and filing sequence are recorded
in `data/raw/`; the names are not. So the person layer is empty because of a choice about
what the evidence supports, not because the data could not be found — and that is a
different and more honest kind of gap.

## 2. Two documents, both written for another purpose

Everything here rests on two regulator notices:

| source | what it was written to do |
|---|---|
| Bank of Ghana, 16 August 2019 | explain why each of 23 institutions had its licence revoked |
| Securities and Exchange Commission, 8 November 2019 | explain why 53 fund managers had theirs revoked |

Neither was written to map ownership across institutions. Each is organised by the entity
being sanctioned, and describes its counterparties only as far as explaining that entity's
own failure requires. **Absence of a relationship in these notices is not evidence that no
relationship exists.** It is evidence that stating it was not necessary to the document's
purpose.

The project has already been caught by this once, in the right direction: reading the Bank
of Ghana notice alone, no entity connected two of the 23. Reading the Commission's notice
as well, one does. That was published as a property of the document — *the notice does not
name one* — rather than as a fact about the world, which is why it could be updated rather
than retracted. The same caution applies to everything still reported as absent.

Sources checked and found to yield nothing are recorded rather than quietly dropped: the
Bank of Ghana's 1 August 2018 universal-bank notice names none of these entities. The
4 January 2019 notice has not been read.

## 3. A quarter of the relationships have an unnamed counterparty

Every edge carries a confidence class, and the counts matter as much as the graph:

- **`documented`** — the source names both ends
- **`documented_unnamed`** — the source states the relationship, often with a count and an
  amount, but does not name the counterparty. *"Related party transactions with eight
  related companies"* is the Bank of Ghana's assertion, not an inference, but the other
  end of the edge is a placeholder node
- **`inferred`** — stated by no source. There are two, both about common ownership implied
  by a shared name. They rest on nothing, carry no citation, and are excluded from every
  figure and from the map

Eighteen of the sixty-nine edges are `documented_unnamed`, and seventeen nodes are
placeholders. Those edges cannot participate in any finding about *who* a counterparty
is, only about how many there were and what moved.

## 4. The graph is in seventeen pieces, and that forbids most network analysis

The related-party graph has 63 nodes in **17 connected components**, the largest holding
10. This is reported rather than worked around, and it rules out the measures a network
project is expected to produce:

- **Betweenness centrality is uninformative.** A node inside a three-node component lies
  on almost no path. The measure is computed and published, and the ranking it produces is
  a property of fragmentation, not a finding about Ghana's savings and loans sector.
- **Community detection returns the components.** Modularity near 0.9 is high *because*
  the graph is fragmented. It discovered nothing.
- **No claim of "one insider network" is available.** The public record describes
  seventeen separate structures.

What carries the analysis instead is the typology of mechanisms, the per-institution
comparison on structural attributes, and three worked examples. Those do not depend on
connectivity — though see section 7 on how much the comparison can actually bear.

## 5. Amounts are barely comparable, and most edges have none

Twenty-nine of sixty-nine edges carry a figure. They are not the same kind of figure:

- 8 exact cedi amounts, 1 stated as a floor
- 20 percentages — shares of a fund manager's own book, which have no currency and cannot
  be converted to one
- of those percentages, 11 are `combined_total`: one share stated across several
  counterparties at once, with no per-counterparty split available

`amount_basis` records *how a figure was stated*, and only exact cedi amounts on
value-extracting edges are ever summed. **GHS 261.72m is quantified across 7 of the 17
flagged institutions.** That is a floor on a floor: it is what two notices happened to
state in cedis, not an estimate of what was extracted. It is also a stock of exposure
rather than a loss — see section 9. The actual losses are much larger and this project
does not estimate them.

One transfer is stated in three currencies at once (USD, GBP and EUR) and is held in a
note rather than as a figure, because the schema will not let three currencies become one
number.

## 6. The placement layer is deliberately excluded from the findings

The Commission's notice describes fund managers placing client money in the 23 with no
related-party claim attached. Thirteen such edges are recorded, and held in a separate
layer that is filtered out of every related-party figure.

Admitting them as ordinary edges would take the graph from **17 components, largest 10**
to **12 components, largest 26**. That would be a far more impressive picture and a less
true one: those institutions share a fund manager who placed client money in both, which
is not evidence that they share an owner.

The consequence runs the other way too. One institution the Bank of Ghana did **not** flag
for related-party exposure — Commerz — appears in the Commission's notice on the receiving
end of a placement its fund manager describes as related-party. The 17-against-6 split is
a property of the Bank of Ghana notice, not of the record.

## 7. The 17-against-6 comparison is a consistency check, not a test

Section 4 of the findings reports that every institution carrying a value-extracting edge
is one of the 17 the Bank of Ghana flagged for related-party exposure, and that none of
the other six carries one. A clean separation on 23 observations looks like a result. It
is not one.

The `related_party_exposure` flag comes from `ghana-banking-collapse`, which coded it from
the Bank of Ghana notice of 16 August 2019. The edges were extracted from **the same
notice**. Two readings of one document agreeing tells you the extraction pipeline neither
dropped an institution nor invented one — genuinely worth knowing, and the reason it is
reported — but it is not corroboration by a second source, and the separation was close to
guaranteed by where both variables come from.

The same caution applies to any future comparison built on these two variables. They are
not independent and must not be treated as though they were.

## 8. "Value moves" is not the same as "value left"

Each relationship type carries an `extracts_value` flag. It means value moves **along the
relationship**. It does not say which way relative to a failed institution, and the two
were conflated once in this repository's own output.

Of the related-party edges, 30 run out of one of the 23. A further 17 either point into an
institution — a fund manager placing client money there moves value *in* — or run between
two parties neither of which is one of the 23, mostly fund managers placing their clients'
money with their own related companies. That last group is a real finding about those fund
managers and a different finding from anything about the 23.

The findings and the page now report direction alongside the flag, and the mechanism
counts include only the edges running out of an institution. The one cycle in which every
leg moves value is called a **circular funding loop** rather than an extraction loop, for
the same reason: value leaves Midland to a related party and that party's client money
funds Midland. Whether either side ended up better off is a question these documents do
not answer.

## 9. Exposure is not loss

Every cedi figure here is a **stock of exposure at a point in time** — a related-party
credit exposure, a liability assumed, a receivable pre-financed. None is a realised loss,
a recovery, or a transfer out of the institution's estate. GHS 160.10m of over-exposure at
uniCredit says the concentration breached the limit, not that GHS 160.10m disappeared.

The figures are also of four incompatible kinds and the schema records which
(`amount_basis`), so nothing sums a floor into an exact figure or a percentage into a cedi
total. But even the cedi total is a heterogeneous aggregate of exposure types, and it
should be described as *quantified related-party exposure the notices happened to state*,
never as an amount extracted.

## 10. Five entity-resolution questions are open

`data/resolution_review.csv` holds five candidates marked `undecided`. Nothing in hand
settles them, and the tooling never merges entities on its own. The one that would change
the graph is whether **Hoda Holdings Ltd**, named by the Commission as a related party of
uniSecurities, is the **Hoda Group of Companies** that the Bank of Ghana says acquired
uniCredit. If they are one entity, a second entity connects two of the 23 and the
uniCredit component closes on itself.

A shared name is not evidence, and none of these are resolved on one. One candidate was
closed at v0.4 on a document rather than on a name: the Commission calls Legacy Capital
Savings a related party of Legacy Fund Management.

## 11. One institution's position is contested

On **21 May 2026 the Court of Appeal quashed** the Bank of Ghana's revocation of GN
Savings and Loans' licence and ordered it restored. The Bank has appealed to the Supreme
Court and the matter is pending.

GN's edges remain in the evidence base, still attributed to the Bank of Ghana, which did
publish those statements. But GN is excluded from the worked examples and carries a status
note wherever it appears, because this project takes no position on live litigation. The
appeal is recorded from press reporting; **the judgment itself has not been read**, and
the source row forbids citing it as evidence for any edge until it is.

## 12. What verification does and does not guarantee

All 69 edges have been checked by hand against the source and the decision recorded in
`data/verification.csv`. The loader additionally refuses to build unless every quote is
verbatim **at the line its anchor names**, and unless a named counterparty is actually
named in the passage cited for its edge.

**The two passes were not identical, and the record says which was which.** The 39 edges
from the Bank of Ghana notice were worked institution by institution from the sheets in
`docs/review/`, each of which pairs an edge with its passage *and* lists every uncited
passage in the same section. The 30 edges from the Commission's notice were checked
against `docs/review/sec/01-sections-with-edges.md`, which reproduces each cited section
in full; the guarantee that nothing was missed comes from a different control there —
`02-coverage.md`, which lists all 53 sections of that notice and flags any that names one
of the 23 without carrying an edge. Per-edge checking shows the edges that exist are
right. Only the coverage sheet shows that the ones that should exist do.

That guarantees the citations are real. It does not guarantee the *reading* is right — a
passage can be quoted correctly and still be interpreted too strongly. Two classes of
judgment are not mechanically checkable and were made by a person:

- whether a passage describes a **relationship** at all, or only a regulatory breach
- whether a placement belongs in the **related-party layer** or the placement layer

The review pack in `docs/review/` exists to make both re-checkable: it lists, beside every
cited passage, every passage in the same section that no edge cites. That is where a
missed relationship would hide, and it has caught one — the Commission's notice was
under-read at v0.3, and eight sections naming one of the 23 went unnoticed until every
section was listed rather than only the cited ones.

## 13. What would change the answer

In rough order of value against effort:

1. **Registrar-General filings** for the holding companies. The only route to the person
   layer this project was conceived around. Needs money and a physical search in Accra.
2. **Receiver's reports and the loan books.** Not public. They would replace
   *"eight related companies"* with eight names.
3. **A document settling `RR007`** — anything stating that UK company 02722739 is the
   affiliate the Bank of Ghana names. A receiver's report, a filed account naming the
   Ghanaian counterparty, or a court listing would do it. Companies House alone gives
   convergence, not identification.
4. **The Bank of Ghana notice of 4 January 2019.** Public, not yet read.
5. **The Court of Appeal judgment of 21 May 2026**, from GhaLII, to replace press
   reporting on GN's status with the document.

**Done, and recorded either way:** UK Companies House (section 1) and the Bank of Ghana's
universal-bank notice of 1 August 2018 (section 2). The first found a strong candidate and
no identification; the second names none of these entities. Both are written down so that
nobody, including a later version of this project, searches them twice.

Nothing in this list is a reason to discount what is here. The point of the list is that
the ceiling on this analysis is a property of the public record, not of the method — and
that where the record is thin, this repository says so rather than filling the gap.
