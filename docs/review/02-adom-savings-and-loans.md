# 2. Adom Savings and Loans Limited

`inst-adom` · notice section **L202–L238** · 2 seeded edge(s) · 10 uncited passage(s)

Read the section in `data/raw/` from L202 to L238, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1 — edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E002 — Adom Savings and Loans Limited → UNNAMED related parties of Adom

| | |
|---|---|
| relationship | `lends_to` |
| amount | — |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L224` |
| current decision | pending |

> Non-performing related party exposures were far in excess of the statutory limits.

*Note carried from compilation:* No amount stated

### E003 — Adom Savings and Loans Limited → UNNAMED related parties of Adom

| | |
|---|---|
| relationship | `pays_management_fees_to` |
| amount | — |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L229` |
| current decision | pending |

> Poor earnings due mainly to high management fees paid to related parties.

*Note carried from compilation:* Fee extraction rather than lending

---

## Part 2a — uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L210`**
  > A review of the institution's performance in August 2018 revealed that it was insolvent. The institution's reported capital adequacy ratio and net worth as at May 2019 were negative. The Bank of Ghana has since August 2018 engaged the Board and Shareholders of the company on the need to inject additional capital.

- **`bog-2019-08-16-savings-loans-revocation:L230`**
  > Weaknesses in Board and Senior Management oversight, including the fact that the institution have been without a substantive Managing Director since September 2018.

---

## Part 2b — the rest of the section (8 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full — the extractor's vocabulary has been wrong twice already, so its judgement about what is irrelevant is not final.

- `L204` Adom Savings and Loans Company Limited is a financial services company incorporated under the Companies Act, 1963 (Act 179) in January 2010 and licens …
- `L215` Among other things, the Bank of Ghana's supervisory assessments revealed the following:
- `L218` The institution's Net worth of negative GHS 9.60 million as at end May 2019 violated section 28(1) of Act 930.
- `L221` The institution's capital adequacy ratio of negative 126.23% as at end May 2019 was in violation of Section 29(2) of Act 930.
- `L225` The Institution has consistently breached the minimum cash reserve ratio
- `L227` requirement since 11th July, 2018 mainly as a result of its liquidity challenges. The institution is also unable to meet withdrawals of customers.
- `L233` Poor credit underwriting standards and weaknesses in risk management function resulting in high non-performing loans.
- `L235` The company did not keep accounting records in a manner that gives an accurate and reliable account of the transactions of the company thus not showin …

