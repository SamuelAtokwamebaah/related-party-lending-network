# 11. First Allied Savings and Loans Limited

`inst-first-allied` · notice section **L538–L594** · 2 seeded edge(s) · 12 uncited passage(s)

Read the section in `data/raw/` from L538 to L594, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1 — edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E013 — First Allied Savings and Loans Limited → UNNAMED major shareholder of First Allied

| | |
|---|---|
| relationship | `controls` |
| amount | — |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L580` |
| current decision | confirmed |

> The current accounts of eight (8) related companies linked to the major shareholder were overdrawn in excess of GHS 100.00 million and were non- performing.

*Note carried from compilation:* Person unnamed; role documented

### E014 — First Allied Savings and Loans Limited → UNNAMED eight related companies of First Allied

| | |
|---|---|
| relationship | `overdrawn_current_accounts` |
| amount | GHS 100.00m (floor) |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L580` |
| current decision | confirmed |

> The current accounts of eight (8) related companies linked to the major shareholder were overdrawn in excess of GHS 100.00 million and were non- performing.

*Note carried from compilation:* Amount is a stated floor not an exact figure

*Amount note:* notice says 'in excess of' GHS 100.00 million

---

## Part 2a — uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L543`**
  > First Allied Savings & Loans Ltd. (FASL) was found to be insolvent with a negative Capital Adequacy Ratio and a negative net worth as of 31 March 2018. The Bank of Ghana directed the Board Chairman/Majority Shareholder and Management of the Institution to immediately inject additional capital to address the capital deficiency. In June 2018, the Bank of Ghana received reports of a run on the institution FASL due to it …

---

## Part 2b — the rest of the section (11 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full — the extractor's vocabulary has been wrong twice already, so its judgement about what is irrelevant is not final.

- `L540` First Allied Savings and Loans Limited (FASL) was licensed by Bank of Ghana to operate as a savings and loans company on March 27, 1996.
- `L555` A review of the institution's operations in July 2018 revealed that its reported financial statements did not reflect its true state of affairs. An ad …
- `L561` The specific issues that led to the revocation of its license included the following:
- `L563` The institution's Net worth of negative GHS 661.84 million as at end May 2019 indicates that its paid up capital is impaired in violation of Section 2 …
- `L566` The institution's capital adequacy ratio of negative 263.21% as at end May 2019 is in violation of Section 29(2) of Act 930.
- `L569` The income surplus and profit & loss accounts per the General Ledger as at 31st August, 2018 showed losses but the institution reported positive Incom …
- `L574` The reported deposit liabilities were grossly understated as at end-June 2018,in effect, reducing customer deposits to conceal losses over the years.
- `L577` Total non-performing loans constituted 88.89% of the institution's total loan portfolio.
- `L584` The Institution purportedly advanced credit facilities to various institutions, predominantly churches and schools without proper documentation. These …
- `L588` The Institution stopped submitting prudential returns to Bank of Ghana in June 2018, citing technical challenges.
- `L591` The Institution cannot meet the deposit withdrawals of its customers with many customer complaints received by the Bank of Ghana.

