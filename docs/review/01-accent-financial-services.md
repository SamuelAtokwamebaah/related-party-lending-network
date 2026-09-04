# 1. Accent Financial Services Limited

`inst-accent` · notice section **L166–L201** · 1 seeded edge(s) · 11 uncited passage(s)

Read the section in `data/raw/` from L166 to L201, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1 — edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E001 — Accent Financial Services Limited → UNNAMED related parties of Accent

| | |
|---|---|
| relationship | `lends_to` |
| amount | — |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L188` |
| current decision | pending |

> Most of the institution's investments portfolio had no supporting documents whilst loans granted to related parties were concealed from the Bank of Ghana.

*Note carried from compilation:* Counterparty identity and count not stated

---

## Part 2a — uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L171`**
  > The institution has been insolvent since March 2017. The Bank of Ghana has since March 2017 engaged the Board and Senior Management of the institution on the need to inject additional capital but that yielded no results.

- **`bog-2019-08-16-savings-loans-revocation:L197`**
  > Corporate governance weaknesses with weak Board and Management oversight.

---

## Part 2b — the rest of the section (9 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full — the extractor's vocabulary has been wrong twice already, so its judgement about what is irrelevant is not final.

- `L168` Accent Financial Services Limited was incorporated in Ghana on 21st November, 2012 and was licensed by the Bank of Ghana to commence operations in Jun …
- `L175` The specific issues that led to the revocation of its license included the following:
- `L177` The institution had a net worth of negative GHS 55.76 million as at end February 2019, in violation of section 28(1) Act 930.
- `L180` The institution had a capital adequacy ratio of negative 144.30% as at end February 2019, in violation of section 29(2) of Act 930.
- `L183` The institution has been facing serious liquidity challenges as it has been unable to meet customer withdrawal requests since 2017. The Bank of Ghana  …
- `L192` High non-performing loans due to poor underwriting standards
- `L193` Creative accounting practices, thereby misrepresenting the institution's true
- `L195` financial condition and thereby misreporting its true financial position to the Bank of Ghana.
- `L199` The institution is currently not engaged in normal business activities as a result of its capital and liquidity challenges.

