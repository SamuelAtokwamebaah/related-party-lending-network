# Verification: what went wrong here, and what caught it

This repository reconstructs a lending network from three public documents. The
only thing that makes such a reconstruction worth anything is whether each edge
says what its source says, so the record of how that was tested is part of the
output rather than an appendix to it.

`data/changelog.csv` carries all 44 changes with the reasoning behind each, and
`data/verification.csv` carries one row per edge with who checked it and when.
This file is the narrower thing: the errors, what each would have cost, and the
mechanism that found it.

It is organised by **what caught it** rather than by who caused it. The project
was built with heavy use of an AI assistant and the history does not record
which lines came from which of us, so blame would be unverifiable in most of
these entries. The mechanism is recoverable in all of them.

Twenty-seven of the forty-four changelog entries are corrections. The ones below
are those where the repository had said something it could not support.

| caught by | entries |
|---|---:|
| feeding the loader deliberately broken data | 1 |
| reading the repository as a risk analyst rather than as its author | 5 |
| re-reading a passage against the edge drawn from it | 4 |
| looking at the rendered output instead of the data | 2 |
| computing a property instead of eyeballing it | 1 |

---

## Caught by feeding the loader deliberately broken data

### 1. Five of the loader's own defences did not work

The validating loader in `scripts/load.py` is the spine of this project. Rule 11
requires that a quoted passage be present, verbatim and in full, at the line its
anchor names. Rule 12 requires that the passage name the counterparty. Both were
tested at v0.7 by constructing data designed to violate them.

**Five faults passed.**

Rule 11 compared only the first 80 characters of a quote, and accepted a match
anywhere within the following 60 lines. So a word altered late in a long quote
passed. An empty quote passed. An anchor placed a few lines early passed.

Rule 12 matched name fragments rather than whole words, so the alias "GN"
matched inside unrelated longer names and satisfied the rule without the
counterparty being named at all.

**What it would have cost.** Every figure in this repository rests on the claim
that each edge is supported by the passage cited beside it, and the loader is
the only thing enforcing that claim. A defence that passes everything is worse
than no defence, because the project had been reporting that its evidence base
was machine-validated.

**Fixed at v0.7.** The whole quote must now start at its anchor, and matching is
whole-word. Recorded as C039.

**The lesson.** A check nobody has watched fail is a comment. Three of the five
faults here are cases where the check was doing something narrower than its
description, which is invisible until you try to break it on purpose.

---

## Caught by reading the repository as a risk analyst rather than as its author

A full review at v0.7 read the evidence base, the analysis and the published
prose as an outside reader would. Every published number tied to the database,
sixteen checked with no failures. What did not hold up was **language**, in
places where the words claimed more than the data.

### 2. The weakest sentence in the repository

> "Built independently from passages, it reproduces the published 17-of-23
> finding."

The `related_party_exposure` flag was coded in `ghana-banking-collapse` from the
Bank of Ghana notice. The edges in this repository were extracted from the same
notice. Two readings of one document agreeing is a **consistency check on the
extraction pipeline**, which is worth reporting, and it is not corroboration by
a second source. A near-perfect separation was close to guaranteed by where both
variables come from.

Said plainly now in the README, the findings and the limitations. Recorded as
part of the v0.7 audit.

This is the entry to read first. It is not an arithmetic error and no figure
changed. The repository was presenting a tautology as a validation, which is a
more serious thing to get wrong than a number.

### 3. A chart that counted the wrong direction

"How value left the institutions" counted every related-party edge. Only **30 of
them run out of one of the 23**. Seventeen either point into an institution, a
fund manager placing client money there moves value in, not out, or run between
two parties neither of which is one of the 23, mostly fund managers placing
clients' money with their own related companies.

The chart now counts only the 30 and says what the other 17 are.

### 4. A definition that invited the mistake in entry 3

`extracts_value` was documented as marking value moving "out of the
institution". It marks value moving **along the relationship**, in whichever
direction the edge points. No figure was wrong, because the view behind the
published profile already restricted to edges leaving one of the 23. But the
definition invited the error, and the chart had made it.

### 5. A metric that named a conclusion the documents do not support

The one cycle in which every leg moves value was called a "closed extraction
loop". Value leaves Midland to a related party, and that party's client money
funds Midland. That is **circular funding** between related parties. Whether
either side ended up better off is not something these documents say, and
"extraction" claimed a direction they do not establish. Renamed
`circular_funding_loops`.

### 6. A category whose name was not the notice's word

`fee_extraction` was renamed `payments`. Management fees, rent and a
shareholder's loan taken onto an institution's books are payments to a related
party. "Extraction" is not the notice's word and claims a direction the
limitations section explicitly withdraws.

---

## Caught by re-reading a passage against the edge drawn from it

### 7. Every line anchor was up to 26 lines out

The Phase 0 extractor used `str.splitlines()`, which also breaks on form feeds.
The Bank of Ghana notice carries **27 of them as page breaks**, so every anchor
ran up to 26 lines ahead of the line that `grep`, `sed` or an editor shows.

**What it would have cost.** Rule 11 checks a quote against the line its anchor
names. If the anchors are systematically offset, every manual verification
against them is checking the wrong line. Corrected at v0.1 before any figure was
published, and three edges were also pointing at the wrong paragraph
independently of the offset. Recorded as C002.

### 8. An edge pointing the wrong way

E013 said First Allied controls its own majority shareholder. The notice names
the institution's "Board Chairman/Majority Shareholder", so the shareholder owns
the institution. Relationship corrected from `controls` to `owns`, anchor moved
to the line where the phrase actually appears. Recorded as C029.

### 9. A role attributed to the wrong party

R003 recorded a company as Crest Finance House's chief executive. The notice says
the chief executive **is a director of** that company, and names neither the
person nor, in that passage, the institution's officer. R003 was removed and the
fact kept in the relevant edge's note. Recorded as C033.

### 10. An arithmetic slip inside a correction note

C009 stated that eight unread sections of the Securities and Exchange Commission
notice named one of the 23. It is nine: of the four sections read at v0.3, two
name one of the 23, so nine remained. The nine fund managers C009 listed were
right; the arithmetic in its last sentence was not. Corrected everywhere the
count appears, as C028.

---

## Caught by looking at the rendered output instead of the data

### 11. The map credited every quotation to the wrong regulator

The published map attributed every quoted passage to the Bank of Ghana,
including **17 from the Securities and Exchange Commission notice** and one from
a Court of Appeal judgment. The same page printed "all edges verified" beside a
provisional banner, and stated that the Commission linked two entities that it
does not.

All corrected at v0.7, with each passage now naming its own source. Recorded as
C040.

This one is worth noting because the data was correct throughout. The defect was
entirely in the layer a reader actually sees, which nothing in the project was
checking.

### 12. Seven edges displayed a heading instead of their evidence

Heading anchors were added at v0.4 to satisfy rule 12, as supporting citations.
The join that built the map took whichever anchor came back first, so hovering
the GHS 160.10m uniCredit edge showed the section heading "22. UNICREDIT GHANA
LIMITED" rather than the passage. Fixed as part of the v0.7 audit.

---

## Caught by computing a property instead of eyeballing it

### 13. Two colours failed accessibility in the theme the author never sees

The map's link colour measured 4.42:1 against white and the citation panel's
muted text measured 4.08:1 against its surface. Both carry text, so both need
4.5:1 under WCAG AA. They failed in the **light** theme, which is the one the
author does not work in and had therefore never looked at.

Found by computing relative luminance for every text token against every surface
it sits on, rather than by looking at the page. Now 4.96 and 4.97 against white.
Recorded as C041.

Included here, although it changes no finding, because it is the clearest case
in any of these repositories of a defect that only a measurement could find. No
amount of careful looking at a dark theme reveals a contrast failure in a light
one.

---

## A decision, not an error

The **person layer is empty by decision**. The UK company register names two
serving directors, several resigned officers and one person with significant
control. Those names are public and are not reproduced here: no regulator has
named any individual in connection with this failure, and the identification
linking the company to it is undecided. Counts, nationalities and filing
sequences are used; names are not. Recorded as C019.

A related correction belongs with it. The map's footer claimed that no
individual is named anywhere in the evidence base. Read strictly that is true of
the CSVs, where the only person node is a placeholder, but the Bank of Ghana
notice reproduced verbatim in `data/raw/` names the Receiver, and so does the
vendored PDF. The claim worth making is the one the project actually enforces,
so the footer now says **no individual appears as a node in this graph**.
Recorded as C042.

---

## What this record does not cover

It does not cover errors nobody has found. The v0.7 audit found four
overstatements and three defects in a repository that had already been verified
edge by edge, so the honest reading is that this list is incomplete and that
the way to extend it is to build the next check.

Related ledgers. Two of these repositories are private while the work in them is unfinished, so they are named rather than linked:

- `thin-file-credit-risk` (private): a train/test split that was never reproducible although every seed was fixed, a refuted prediction, a feature built on a false premise, and an exit code swallowed by a pipe.
- `act-930-resolution-timelines` (private): an abstract that contradicted the method section, twice, and a paper that misdescribed its own companion dataset.
- [`ghana-banking-collapse`](https://github.com/SamuelAtokwamebaah/ghana-banking-collapse/blob/main/docs/verification.md)
- [`microfinance-fraud-detection`](https://github.com/SamuelAtokwamebaah/microfinance-fraud-detection/blob/main/docs/verification.md)
