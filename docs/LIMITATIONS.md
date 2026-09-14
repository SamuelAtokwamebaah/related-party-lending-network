# Limitations

What this project cannot show, and why. Written to be read on its own, before or instead
of the findings.

Figures are as at evidence base `v0.7`. `docs/phase2/metrics.json` is authoritative if
this document and the data ever disagree; every claim below is checkable against `data/`
and, except for the GN judgment (section 11), the documents in `sources/`.

---

## 1. It names no individuals, and it was supposed to

The project was conceived to model insider relationships: who owned the institutions that
failed, who sat on their boards, and whether the same people appear behind more than one
failure. **The evidence base contains no named person.** The one `person` node in the
graph is a placeholder — *"UNNAMED major shareholder of First Allied"*, whom the notice also
calls the Board Chairman — because that is exactly as far as the Bank of Ghana's notice
goes. The majority shareholder of Global Access is also a placeholder, and is not typed as
a person, because the notice does not say whether it is one.

This is the single largest gap, and no amount of analysis closes it. What the graph
actually models is **relationships between companies**: institutions, their holding
companies, their group affiliates and their fund managers. That is a real structure and it
is worth reading. It is not the ownership network the project set out to build, and the
network diagrams should not be read as though a person sits behind each node.

Two kinds of name are citations rather than subjects, and appear where the documents
carry them: the receiver the Bank of Ghana appointed, named in its own notice, and the
parties' names in the title of a published judgment cited in section 13.

Building the person layer needs the Registrar-General's company filings. Ghana's register
is not freely searchable online; the realistic route is a paid physical search in Accra.

**UK Companies House has now been searched, and the layer is still empty — by decision.**
The register holds FIRST AFRICAN REMITTANCES LIMITED (02722739), incorporated 12 June 1992
as First African Forex Bureau Limited, in financial intermediation, dissolved by voluntary
strike-off on 22 October 2019. It names two directors serving at dissolution, both
recorded as Ghanaian nationals resident in Ghana, with a correspondence address in Accra,
and one person with significant control.

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

The company's last filed accounts and its annual returns were also examined, and
deliberately not vendored for the same reason — they name individuals and shareholdings.
The relevant negative is recorded in the changelog: **the accounts contain no related-party
note, name no Ghanaian counterparty, and mention no sum resembling the GHS 5.40m.** They do
not settle `RR007` either.

**At v0.6 a document did name individuals, and the layer is still empty.** The Court of
Appeal judgment on GN Savings and Loans (21 May 2026) names individuals, among them a
shareholder of the companies involved, and describes their roles. For this one
institution the first reason above no longer holds: a document now makes the connection.
The layer stays empty for a different reason. GN is the one institution where the latest
decision found the revocation unjustified, and that decision is itself stayed pending
appeal. Putting individuals connected to GN into a graph of the insider relationships
behind the failures would imply a conclusion the most recent judgment cuts against. The
judgment is not vendored, for the same reason the filings above were not, and its
transcription replaces names with bracketed descriptions.

## 2. Two documents, both written for another purpose

Everything here but one edge rests on two regulator notices:

| source | what it was written to do |
|---|---|
| Bank of Ghana, 16 August 2019 | explain why each of 23 institutions had its licence revoked |
| Securities and Exchange Commission, 8 November 2019 | explain why 53 fund managers had theirs revoked |

The exception is `E044`, GN Savings and Loans' membership of Groupe Nduom, taken from the
Court of Appeal judgment of 21 May 2026. A judgment is written for another purpose too:
it describes the parties only as far as deciding the dispute requires.

Neither notice was written to map ownership across institutions. Each is organised by the
entity being sanctioned, and describes its counterparties only as far as explaining that
entity's own failure requires. **Absence of a relationship in these notices is not evidence
that no relationship exists.** It is evidence that stating it was not necessary to the
document's purpose.

The project has already been caught by this once, in the right direction: reading the Bank
of Ghana notice alone, no entity connected two of the 23. Reading the Commission's notice
as well, one does. That was published as a property of the document — *the notice does not
name one* — rather than as a fact about the world, which is why it could be updated rather
than retracted. The same caution applies to everything still reported as absent.

Sources checked and found to yield nothing are recorded rather than quietly dropped: the
Bank of Ghana's 1 August 2018 universal-bank notice names none of these entities. The
4 January 2019 notice has not been read.

## 3. A third of the relationships have an unnamed counterparty

Every edge carries a confidence class, and the counts matter as much as the graph:

- **`documented`** — the source names both ends
- **`documented_unnamed`** — the source states the relationship, often with a count and an
  amount, but does not name the counterparty. *"Related party transactions with eight
  related companies"* is the Bank of Ghana's assertion, not an inference, but the other
  end of the edge is a placeholder node
- **`inferred`** — stated by no source. There are two. One is common ownership implied by
  a shared name (Ideal Financial Holdings and Ideal Finance); the other rests on a sibling
  relationship and a 2006 acquisition (the Hoda Group and uniSecurities). They carry no
  citation, and are excluded from every figure and from the map

Twenty-five of the seventy-five edges are `documented_unnamed`, and eighteen nodes are
placeholders. Those edges cannot participate in any finding about *who* a counterparty
is, only about how many there were and what moved.

## 4. The graph is in seventeen pieces, and that forbids most network analysis

The related-party graph has 64 nodes in **17 connected components**, the largest holding
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

Twenty-nine of seventy-five edges carry a figure. They are not the same kind of figure:

- 8 exact cedi amounts, 1 stated as a floor
- 20 percentages — shares of a fund manager's own book, which have no currency and cannot
  be converted to one
- of those percentages, 11 are `combined_total`: one share stated across several
  counterparties at once, with no per-counterparty split available

`amount_basis` records *how a figure was stated*, and only exact cedi amounts on
value-moving edges out of an institution are ever summed. **GHS 261.72m is quantified
across 7 of the 17 flagged institutions.** That is a floor on a floor: it is what the Bank
of Ghana notice happened to state in cedis, not an estimate of what was lost. It is also a
stock of exposure rather than a loss — see section 9 — and it adds figures from different
dates: one of them, GHS 52.70m at Ideal Finance, comes from an onsite examination of
September 2017. The actual losses are much larger and this project does not estimate them.

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
end of a placement the Commission describes as related-party. The 17-against-6 split is a
property of the Bank of Ghana notice, not of the record.

## 7. The 17-against-6 comparison is a consistency check, not a test

Section 4 of the findings reports that every institution carrying a value-moving edge out
is one of the 17 the Bank of Ghana flagged for related-party exposure, and that none of the
other six carries one. A clean separation on 23 observations looks like a result. It is
not one.

The `related_party_exposure` flag comes from `ghana-banking-collapse`, which coded it from
the Bank of Ghana notice of 16 August 2019. The edges were extracted from **the same
notice**. Two readings of one document agreeing tells you the extraction pipeline neither
dropped an institution nor invented one — genuinely worth knowing, and the reason it is
reported — but it is not corroboration by a second source, and the separation was close to
guaranteed by where both variables come from.

The same caution applies to any future comparison built on these two variables. They are
not independent and must not be treated as though they were.

## 8. "Value moves" is not the same as "value left"

Each relationship type carries an `extracts_value` flag. Despite its name, it means value
moves **along the relationship**. It does not say which way relative to a failed
institution, and the two were conflated once in this repository's own output. The prose
calls these edges *value-moving* for that reason.

Of the related-party edges that move value, 34 run out of one of the 23. The other 17
either point into an institution — a fund manager placing client money there moves value
*in* — or run between two parties neither of which is one of the 23, mostly fund managers
placing their clients' money with their own related companies. That last group is a real
finding about those fund managers and a different finding from anything about the 23.

The findings and the page now report direction alongside the flag, and the mechanism
counts include only the edges running out of an institution. The one cycle in which every
leg moves value is called a **circular funding loop**, for the same reason: value leaves
Midland to a related party and that party's client money funds Midland. Whether either
side ended up better off is a question these documents do not answer.

## 9. Exposure is not loss

Every cedi figure here is a **stock of exposure at a point in time** — a related-party
credit exposure, a liability assumed, a receivable pre-financed. None is a realised loss,
a recovery, or a transfer out of the institution's estate. GHS 160.10m of over-exposure at
uniCredit says the concentration breached the limit, not that GHS 160.10m disappeared.

The figures are also of four incompatible kinds and the schema records which
(`amount_basis`), so nothing sums a floor into an exact figure or a percentage into a cedi
total. But even the cedi total is a heterogeneous aggregate of exposure types, and it
should be described as *quantified related-party exposure the notices happened to state*,
never as an amount extracted or lost.

## 10. Five entity-resolution questions are open, and four matches rest on a rule

`data/resolution_review.csv` holds seven candidates, five of them marked `undecided`.
`RR007` was added at v0.5 and is discussed in section 1. Nothing in hand settles the five,
and the tooling never merges entities on its own. The one with the largest structural
consequence is whether **Hoda Holdings Ltd**, named by the Commission as a related party of
Unisecurities (Ghana) Limited, is the **Hoda Group of Companies** that the Bank of Ghana
says acquired uniCredit. If they are one entity, the record connects uniCredit to
uniSecurities through a common owner and the uniCredit component closes on itself. It
would still link only one of the 23.

A shared name is not evidence, and none of these are resolved on one. Two candidates are
closed, each on a document: at v0.4 the Commission calls Legacy Capital Savings a related
party of Legacy Fund Management, so they are two firms; at v0.7 the Bank of Ghana lists
Commerz and Sterling Financial Services as two separate licensees, revoked on the same day.

**Matching across documents follows a stated rule.** Where two documents use the same legal
name — allowing for punctuation, case and a jurisdiction suffix — they are treated as the
same entity. Where the names differ, the match is made only on a document, and otherwise
becomes a resolution candidate. Every edge linking the SEC notice to the Bank of Ghana's
entities depends on this rule, and the strength behind each match is not the same:

- **Gold Coast Fund Management**: matched on a document. The Bank of Ghana calls it SEC
  licensed and "now Blackshield Capital Management"; the Commission's section is
  "Blackshield Capital Management Ltd (formerly Gold Coast Fund Management Limited)".
- **Liberty Asset Management**: same name, and the two notices corroborate each other —
  each names the other side of the Midland relationship.
- **Ideal Capital Partners**: same name, and the Commission's section names Ideal Financial
  Holdings and FirsTrust as its related parties.
- **uniSecurities**: same name only. The Commission's section on Unisecurities (Ghana)
  Limited names neither uniCredit nor the Hoda Group. If this match were wrong, the seven
  edges S007 to S013 would leave the uniCredit component, and the largest structure in the
  graph would split in two.

The Commission's section on All-Time Capital Limited shares a name with a node the Bank of
Ghana names, but it states no relationship to AllTime Finance or to any of the 23, so no
edge comes from it.

## 11. One institution's position is contested

On **21 May 2026 the Court of Appeal quashed** the Bank of Ghana's revocation of GN
Savings and Loans' licence and ordered it restored. On **14 July 2026 the Supreme Court
stayed** that judgment pending the Bank of Ghana's appeal, so the licence has not been
restored and the matter is live.

The Court of Appeal judgment has been read, from a certified true copy. The stay is
recorded from press reporting; no document is in hand.

GN's Bank of Ghana edges remain in the evidence base, still attributed to the Bank, which
did publish those statements. One edge, `E044`, is attributed to the Court of Appeal, and
it records only that GN was a member of Groupe Nduom, which the court treats as
undisputed. Nothing the judgment says about solvency, valuation or the fairness of the
revocation enters the evidence base, because that is what the appeal is about. GN is
excluded from the worked examples and carries a status note wherever it appears.

## 12. What verification does and does not guarantee

All 75 edges have been checked by hand against the source and the decision recorded in
`data/verification.csv`. The loader additionally refuses to build unless every quote is
verbatim, in full, **at the line its anchor names**, and unless a named counterparty is
named, as whole words, in the passage cited for its edge.

**The passes were not identical, and the record says which was which.** The 39 edges of
the first pass — 37 from the Bank of Ghana notice and the two inferred edges — were worked
institution by institution from the sheets in `docs/review/`, each of which pairs an edge
with its passage *and* lists every uncited passage in the same section. Two of them, `E043`
and `I002`, touch no institution and so appear on no sheet; `E043`'s passage is shown on the
GN sheet beside `E042`. The 30 edges from the Commission's notice were checked against
`docs/review/sec/01-sections-with-edges.md`, which reproduces each cited section in full;
the guarantee that nothing was missed comes from a different control there —
`02-coverage.md`, which lists all 53 sections of that notice and flags any that names one
of the 23 without carrying an edge. Per-edge checking shows the edges that exist are
right. Only the coverage sheet shows that the ones that should exist do.

The one edge from the Court of Appeal judgment, `E044`, had a third kind of check. The
judgment is a scan with no text layer, so rule 11 checks its quotes against the
transcription in `data/raw/`, and a person checked the transcription against the scan by
printed page number, from `docs/review/ca-2026-05-21-gn-judgment.md`. The scan is not in
this repository, so a reader cannot repeat that check here.

**The pre-release audit at v0.7 was a fourth pass, and it found things the others had
not.** One edge ran the wrong way, two were in the wrong confidence class, two used a
relationship stronger than the text, and five relationships the notice states had no
edge. Every edge whose reading changed, and every edge added, was set back to `pending`
and checked again by hand. The same audit fed the loader deliberately broken data, and
found that rule 11 had been checking only the first 80 characters of a quote. Until v0.7,
then, a citation guaranteed its quote began correctly, not that all of it was verbatim.
Every quote passes the stricter rule.

That guarantees the citations are real. It does not guarantee the *reading* is right — a
passage can be quoted correctly and still be interpreted too strongly. Two classes of
judgment are not mechanically checkable and were made by a person:

- whether a passage describes a **relationship** at all, or only a regulatory breach
- whether a placement belongs in the **related-party layer** or the placement layer

The review pack in `docs/review/` exists to make both re-checkable: it lists, beside every
cited passage, every passage in the same section that no edge cites. That is where a
missed relationship would hide, and it has caught one — the Commission's notice was
under-read at v0.3, and nine sections naming one of the 23 went unnoticed until every
section was listed rather than only the cited ones. It has limits too. Three of the five
relationships the audit added sat in passages already cited for a different edge, which
the pack does not list as uncited.

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
4. **A document settling the uniSecurities match** — anything in the Commission's record
   connecting Unisecurities (Ghana) Limited to uniCredit or the Hoda Group (section 10).
5. **The Bank of Ghana notice of 4 January 2019.** Public, not yet read.
6. **The Supreme Court's decision on GN**, or its stay order of 14 July 2026, to replace
   press reporting on the stay with the document.

**Done, and recorded either way:** UK Companies House (section 1), the Bank of Ghana's
universal-bank notice of 1 August 2018 (section 2), the Court of Appeal judgment in
*Kohl v Consolidated Bank Ghana* (Civil Appeal No H1/95/2021, 2022), and the Court of
Appeal judgment on GN of 21 May 2026 (section 11). The first found a strong candidate and
no identification; the second and third name none of these entities; the fourth added one
edge. All four are written down so that nobody, including a later version of this
project, searches them twice.

Nothing in this list is a reason to discount what is here. The point of the list is that
the ceiling on this analysis is a property of the public record, not of the method — and
that where the record is thin, this repository says so rather than filling the gap.
