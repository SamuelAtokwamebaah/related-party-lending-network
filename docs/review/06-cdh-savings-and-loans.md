# 6. CDH Savings and Loans Ltd.

`inst-cdh` · notice section **L338–L384** · 3 seeded edge(s) · 6 uncited passage(s)

Read the section in `data/raw/` from L338 to L384, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1 — edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E006 — CDH Savings and Loans Ltd. → Ivory Finance Company Limited

| | |
|---|---|
| relationship | `succeeded` |
| amount | — |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L340` |
| current decision | pending |

> CDH Savings and Loans Limited commenced operations in 2016 after taking over Ivory Finance Company Limited which had been operating since the year 2000. In September 2018, CDH Savings & Loans Limited (CDH) was identified as insolvent per the August 2018 prudential returns submitted. CDH itself reported a negative Capital Adequacy Ratio which was further adjusted downward by the Bank of Ghana. The Bank of Ghana also noted severe liquidity challenges which threatens the ability of the institution to operate as a going concern as an additional issue. The Bank of Ghana has since engaged extensively the Board and Senior Management on the need to inject additional capital into the company, and plans repeatedly submitted by CDH to the Bank of Ghana to address supervisory concerns have failed to materialise.

*Note carried from compilation:* Corporate succession not a related-party edge

### E007 — CDH Savings and Loans Ltd. → UNNAMED affiliates of CDH

| | |
|---|---|
| relationship | `transferred_collateral_to` |
| amount | — |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L368` |
| current decision | pending |

> The transfer of collateral security supporting the institution's non-performing loans/exposures to affiliate companies using creative accounting with no resultant cash inflow to the company which resulted in the overstatement of the balance sheet.

*Note carried from compilation:* Asset-stripping pattern

### E008 — CDH Savings and Loans Ltd. → UNNAMED affiliates of CDH

| | |
|---|---|
| relationship | `over_exposed_to` |
| amount | — |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L373` |
| current decision | pending |

> The overexposure of CDH to its affiliate companies to the tune of 319% contrary to the regulatory limit of 25%.

*Note carried from compilation:* Ratio stated not an amount; count not stated

---

## Part 2a — uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L361`**
  > The recognition of income on non-performing loans/exposures by the company contrary to Directives of the Bank of Ghana. Income on non-performing loans/exposures were to be suspended until such time as the loans/exposures became performing but CDH did not comply with this Directive, resulting in an overstatement of its revenue and assets in the financial statements over several years.

- **`bog-2019-08-16-savings-loans-revocation:L381`**
  > The inability of CDH to access placements/investments with other insolvent financial institutions, including related companies, worsened its solvency liquidity situation.

---

## Part 2b — the rest of the section (4 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full — the extractor's vocabulary has been wrong twice already, so its judgement about what is irrelevant is not final.

- `L352` The Specific issues which led to the revocation of the company's license are the following:
- `L355` The institution's Net worth of negative GHS 171.36 million as at end May 2019 violated Section 28(1) Act 930.
- `L358` The institution's capital adequacy ratio of negative 35.90% as at end May 2019 was in violation of Section 29(2) of Act 930.
- `L376` The failure of CDH to sell repossessed collaterals caused liquidity challenges resulting in the company's inability to meet withdrawal requests from n …

