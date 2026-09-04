# 15. Global Access Savings and Loans Company Limited

`inst-global-access` · notice section **L713–L753** · 2 seeded edge(s) · 10 uncited passage(s)

Read the section in `data/raw/` from L713 to L753, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1 — edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E019 — Global Access Savings and Loans Company Limited → UNNAMED majority shareholder of Global Access

| | |
|---|---|
| relationship | `assumed_liability_of_loan_of` |
| amount | GHS 2.91m (exact) |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L737` |
| current decision | pending |

> The institution assumed the liability of a loan contracted by the majority shareholder amounting GHS 2.91 million. The loan amount was injected into the institution as equity capital. The liability was however concealed as a suspense account in the books of Global Access Savings and Loans Limited.

*Note carried from compilation:* Concealed in a suspense account

### E020 — Global Access Savings and Loans Company Limited → UNNAMED majority shareholder of Global Access

| | |
|---|---|
| relationship | `pays_rent_to` |
| amount | — |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L741` |
| current decision | pending |

> The institution continues to record accumulated losses due mainly to high rent expenses paid to the majority shareholder for the use of its premises.

*Note carried from compilation:* Fee extraction; no amount stated

---

## Part 2a — uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L723`**
  > The institution has been insolvent since 2016 with serious liquidity challenges. The reported capital adequacy ratio and net worth are both negative. The Bank of Ghana has had several engagements with the Board and Senior Management on the need to inject additional capital but have not yielded any fruitful results. The institution rather opted to apply for liquidity support from the Bank of Ghana which was declined d …

---

## Part 2b — the rest of the section (9 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full — the extractor's vocabulary has been wrong twice already, so its judgement about what is irrelevant is not final.

- `L715` Global Access Savings and Loans Company Limited was incorporated under the laws of Ghana in 1998 and commenced business in February 2000 as a Partner  …
- `L730` The specific issues that led to the revocation of its license included the following:
- `L731` The institution's Net worth of negative GHS 58.19 million as at end May 2019 indicates that its paid up capital is impaired in violation of Section 28 …
- `L733` The institution's capital adequacy ratio of negative 195.06% as at end May 2019 is in violation of Section 29(2) of Act 930.
- `L735` The institution has breached the statutory cash reserve ratio requirement since 2016.
- `L743` The institution failed to keep accounting records in a manner that gives an accurate and reliable account of its transactions constitutes unsafe and u …
- `L746` The institution failed to implement Bank of Ghana's on-site examinations findings conducted in October 2018.
- `L748` There have been several complaints from customers about the inability of the Institution to honour depositors' withdrawals.
- `L750` The company neither published nor submitted its 2017 Audited Financial Statements to the Bank of Ghana contrary to Act 930.

