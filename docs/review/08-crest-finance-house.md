# 8. Crest Finance House Limited

`inst-crest` · notice section **L415–L449** · 3 seeded edge(s) · 11 uncited passage(s)

Read the section in `data/raw/` from L415 to L449, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1 — edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E009 — Crest Finance House Limited → UNNAMED parent company of Crest

| | |
|---|---|
| relationship | `over_exposed_to` |
| amount | — |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L434` |
| current decision | confirmed |

> Non-performing exposures to its parent company and a company in which the Chief Executive Officer is a director in excess of statutory limit. The exposures also contributed significantly to the institution's liquidity challenges.

*Note carried from compilation:* Exactly one parent implied

### E010 — Crest Finance House Limited → UNNAMED company in which the Crest CEO is a director

| | |
|---|---|
| relationship | `over_exposed_to` |
| amount | — |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L434` |
| current decision | confirmed |

> Non-performing exposures to its parent company and a company in which the Chief Executive Officer is a director in excess of statutory limit. The exposures also contributed significantly to the institution's liquidity challenges.

*Note carried from compilation:* Exposure to a company in which Crest's chief executive is a director; neither the company nor the chief executive is named

### E047 — Crest Finance House Limited ← UNNAMED parent company of Crest

| | |
|---|---|
| relationship | `owns` |
| amount | — |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L434` |
| current decision | confirmed |

> Non-performing exposures to its parent company and a company in which the Chief Executive Officer is a director in excess of statutory limit. The exposures also contributed significantly to the institution's liquidity challenges.

*Note carried from compilation:* 'its parent company'; identity and shareholding not stated

---

## Part 2a — uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L417`**
  > Crest Finance House Limited was originally incorporated as Apex Finance House Limited on September 2, 1997. The name was changed from Apex Finance House Limited to Crest Finance House Limited and subsequently licensed to operate as a Finance House on 5th June 2007.

- **`bog-2019-08-16-savings-loans-revocation:L438`**
  > The institution's total loan portfolio was non-performing due to poor loan underwriting standards and related party exposures.

---

## Part 2b — the rest of the section (9 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full — the extractor's vocabulary has been wrong twice already, so its judgement about what is irrelevant is not final.

- `L422` In 2015, Bank of Ghana found the institution to be insolvent with serious liquidity challenges. The institution's capital adequacy ratio and net worth …
- `L426` The specific issues that led to the revocation of its license included the following:
- `L428` The institution's Net worth of negative GHS 17.55 million as at end May 2019 indicates that its paid up capital is impaired in violation of Section 28 …
- `L431` The institution's capital adequacy ratio of negative 6,873.50% as at end May 2019 is in violation of Section 29(2) of Act 930.
- `L441` The institution was unable to honour its customers' withdrawal request.
- `L442` Weaknesses in corporate governance practices and poor risk management culture
- `L444` contributed to the institution's problems.
- `L445` The institution has ceased operations and closed its offices to the general public,
- `L447` without approval from the Bank of Ghana.

