# 10. Express Savings and Loan Limited

`inst-express` · notice section **L500–L537** · 1 seeded edge(s) · 10 uncited passage(s)

Read the section in `data/raw/` from L500 to L537, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1 — edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E012 — Express Savings and Loan Limited → UNNAMED related parties of Express

| | |
|---|---|
| relationship | `placed_funds_with` |
| amount | — |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L528` |
| current decision | confirmed |

> The institution is overexposed to its related parties with regards placements.

*Note carried from compilation:* No amount stated

---

## Part 2a — uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L505`**
  > The institution has remained insolvent since 2016 due to the inability of the shareholders to inject additional capital into the company. The institution has failed to meet the capital plan submitted to the Bank of Ghana in February 2018 requiring the institution to inject additional capital by end-April 2018 and subsequently to the required minimum. The institution's adjusted capital adequacy ratio and net worth are …

---

## Part 2b — the rest of the section (9 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full — the extractor's vocabulary has been wrong twice already, so its judgement about what is irrelevant is not final.

- `L502` Express Savings and Loans Company Limited (ESLL) was licensed by the Bank of Ghana on 14th August, 2007.
- `L512` The specific issues that resulted in the revocation of the institution's license include the following:
- `L515` The institution is insolvent and has consistently failed to meet the minimum Capital Adequacy Ratio requirement since 2016 due to accumulated losses.
- `L518` The institution's Net worth of negative GHS 119.83 million as at end May 2019 indicates that its paid up capital is impaired in violation of Section 2 …
- `L521` The institution's capital adequacy ratio of negative 610.52% as at end May 2019 is in violation of Section 29(2) of Act 930.
- `L524` The institution has persistently failed to meet the minimum cash reserve ratio requirement and customer withdrawal requests since 2014. Cash reserve r …
- `L529` The institution has failed to submit as well as publish its audited financial statements
- `L531` since 2016 in breach of Act 930, which requires financial institutions to publish and furnish Bank of Ghana with a copy of their audited financial sta …
- `L534` The institution has closed down fourteen (14) of its eighteen (18) branches as at May, 2019 without prior approval from the Bank of Ghana in breach of …

