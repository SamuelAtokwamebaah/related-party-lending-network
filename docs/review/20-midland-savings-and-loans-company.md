# 20. Midland Savings and Loans Company Limited

`inst-midland` · notice section **L1040–L1085** · 3 seeded edge(s) · 10 uncited passage(s)

Read the section in `data/raw/` from L1040 to L1085, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1 — edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E028 — Midland Savings and Loans Company Limited → Liberty Asset Management

| | |
|---|---|
| relationship | `over_exposed_to` |
| amount | — |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L1065` |
| current decision | pending |

> The institution is over exposed to related parties such as Liberty Asset Management, Liberty DMI Microfinance and Griffin Financial Services continue to be rolled over in spite of the liquidity challenges it faces.

*Note carried from compilation:* Named; no amount

### E029 — Midland Savings and Loans Company Limited → Liberty DMI Microfinance

| | |
|---|---|
| relationship | `over_exposed_to` |
| amount | — |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L1065` |
| current decision | pending |

> The institution is over exposed to related parties such as Liberty Asset Management, Liberty DMI Microfinance and Griffin Financial Services continue to be rolled over in spite of the liquidity challenges it faces.

*Note carried from compilation:* Named; no amount

### E030 — Midland Savings and Loans Company Limited → Griffin Financial Services

| | |
|---|---|
| relationship | `over_exposed_to` |
| amount | — |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L1065` |
| current decision | pending |

> The institution is over exposed to related parties such as Liberty Asset Management, Liberty DMI Microfinance and Griffin Financial Services continue to be rolled over in spite of the liquidity challenges it faces.

*Note carried from compilation:* Notice says "such as", so the list is not exhaustive

---

## Part 2a — uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L1046`**
  > The institution was found to be facing liquidity challenges in January 2017. A subsequent assessment indicated that the institution was undercapitalized and also facing serious liquidity challenges. The Bank of Ghana has since August 2018, engaged the Board and Senior Management on the need to inject additional capital.

---

## Part 2b — the rest of the section (9 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full — the extractor's vocabulary has been wrong twice already, so its judgement about what is irrelevant is not final.

- `L1042` Midland Savings and Loan Company Limited was licensed by the Bank of Ghana to operate as a Savings and Loans Company on October 21, 1996. It commenced …
- `L1051` The specific issues that led to the revocation of the institution's licence included the following:
- `L1054` The institution's Net worth of negative GHS 148.92 million as at end May 2019 indicates that its paid up capital is impaired in violation of Section 2 …
- `L1057` The institution's capital adequacy ratio of negative 311.91% as at end May 2019 is in violation of Section 29(2) of Act 930.
- `L1060` The institution failed to conduct due diligence on counter parties resulting in the impairment of some investments. In addition to the impairment of t …
- `L1069` The company has consistently breached the minimum cash reserve ratio requirement. Cash reserve requirement as at end May 2019 was 0.23%.
- `L1072` The company failed to keep accounting records in a manner that gives an accurate and reliable account of its transactions. As a result, the institutio …
- `L1078` As a result of the liquidity challenges, the company is unable to provide adequate funds to run the various branches thus rendering the branches inact …
- `L1082` The inability of the company to honour customers' withdrawal request have resulted in customers resorting the use of their lawyers in filing claims on …

