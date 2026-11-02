# 22. uniCredit Ghana Limited

`inst-unicredit` · notice section **L1100–L1140** · 2 seeded edge(s) · 6 uncited passage(s)

Read the section in `data/raw/` from L1100 to L1140, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1: edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E032: uniCredit Ghana Limited → uniSecurities Limited

| | |
|---|---|
| relationship | `over_exposed_to` |
| amount | GHS 160.10m (exact) |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L1127; bog-2019-08-16-savings-loans-revocation:L1100; bog-2019-08-16-savings-loans-revocation:L1108` |
| current decision | confirmed |

> The institution's adjusted capital adequacy ratio of negative 97.83% as at end May 2019 is in violation of Section 29(2) of Act 930. This is mainly due to the non- performing related party exposures of GHS 160.10 million to uniSecurities which is far in excess of its negative networth.

> 22. UNICREDIT GHANA LIMITED

> The Institution is currently over exposed to a related party, uniSecurities Limited, a sister company.

*Note carried from compilation:* Largest single named-counterparty exposure in the notice

### E039: uniCredit Ghana Limited ← Hoda Group of Companies

| | |
|---|---|
| relationship | `acquired` |
| amount | not stated |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L1102` |
| current decision | confirmed |

> uniCredit Ghana Limited (uniCredit), formerly Kantamanto Savings and Loans Company Limited, was given an operating license in October 1995 and commenced operations on 1st November, 1995. In 2006, the Institution was acquired by the Hoda Group of Companies and subsequently its name was changed from Kantamanto Savings and Loans Limited to uniCredit Ghana Limited in March 2007.

*Note carried from compilation:* Acquisition dated 2006

---

## Part 2a: uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L1113`**
  > uniCredit Savings & Loans Ltd. was found to be insolvent with a negative capital adequacy ratio and negative networth following the Bank of Ghana's assessment as of December 2018. The Bank of Ghana directed the Board and Management of the institution to immediately inject additional capital to address the capital deficiency but this has not been successful.

---

## Part 2b: the rest of the section (5 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full, because the extractor's vocabulary has been wrong twice already and its judgement about what is irrelevant is not final.

- `L1119` The specific issues that led to the revocation of the licence of the institution included the following:
- `L1123` The institution's adjusted Net worth of negative GHS 221.32 million as at end May 2019 indicates that its paid up capital is impaired in violation of  …
- `L1132` The Institution has been breaching the statutory cash reserve ratio requirement since April 2018.
- `L1135` The institution is unable to meet the deposit withdrawals of customers due to its severe liquidity challenges. The Bank of Ghana has been receiving ma …
- `L1139` The institution has a high percentage of non-performing loans.

