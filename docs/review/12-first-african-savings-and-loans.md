# 12. First African Savings and Loans Limited

`inst-first-african` · notice section **L595–L632** · 2 seeded edge(s) · 8 uncited passage(s)

Read the section in `data/raw/` from L595 to L632, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1 — edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E015 — First African Savings and Loans Limited → First African Remittances, UK

| | |
|---|---|
| relationship | `pre_financed_receivable_from` |
| amount | GHS 5.40m (exact) |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L618` |
| current decision | confirmed |

> The company's affiliate, First African Remittances, UK failed to reimburse funds totalling GHS 5.40 million due to First African Savings and Loans. First African Savings and Loans pre-financed remittance receivables and the said amount has been outstanding for over two years. The long outstanding remittance receivable has been provisioned as a loss.

*Note carried from compilation:* Named foreign affiliate

### E016 — First African Savings and Loans Limited → UNNAMED related parties of First African

| | |
|---|---|
| relationship | `related_party_exposure_to` |
| amount | — |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L630` |
| current decision | confirmed |

> The institution is unable to meet the withdrawal demands of its depositors. The institution has related party exposure which it is unable to recover.

*Note carried from compilation:* Related party exposure the institution is unable to recover; its form is not stated. May overlap E015

---

## Part 2a — uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L601`**
  > The company was found to be experiencing liquidity and capital adequacy challenges since 2017. In addition, the Bank of Ghana determined in August 2017 and December 2018 confirmed that the company was insolvent. The Bank of Ghana has since October 2018 engaged the Board and Senior Management on the need to inject additional capital.

---

## Part 2b — the rest of the section (7 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full — the extractor's vocabulary has been wrong twice already, so its judgement about what is irrelevant is not final.

- `L597` First African Savings & Loans Company Limited was incorporated in November 1993 to undertake money transfer and remittance business. It was licensed b …
- `L607` The specific issues that led to the revocation of its licence included the following:
- `L609` The institution's Net worth of negative GHS 22.29 million as at end May 2019 indicates that its paid up capital is impaired in violation of Section 28 …
- `L612` The institution's capital adequacy ratio of negative 90.15% as at end May 2019 is in violation of Section 29(2) of Act 930.
- `L615` The company failed to conduct due diligence on its counterparties resulting in the impairment of some of its investments.
- `L624` The company's Non-Performing Loans ratio has been deteriorating since 2017 to virtually 100% non-performing at end May 2019.
- `L627` The company has consistently violated the minimum cash reserve ratio requirement, which is the regulatory measure of the liquidity position of deposit …

