# 5. ASN Financial Services Limited

`inst-asn` · notice section **L306–L337** · 1 seeded edge(s) · 10 uncited passage(s)

Read the section in `data/raw/` from L306 to L337, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1 — edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E031 — ASN Financial Services Limited → UNNAMED related party projects of ASN

| | |
|---|---|
| relationship | `funded_projects_of` |
| amount | — |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L329` |
| current decision | confirmed |

> The use of depositors' funds to finance some related party projects.

*Note carried from compilation:* No amount stated

---

## Part 2a — uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L311`**
  > The institution has remained insolvent with serious liquidity challenges since October 2016. Its capital adequacy ratio and net worth as at end-June2019 were negative. The Bank of Ghana has engaged the shareholders several times on the need to inject additional capital to rectify the capital deficiency. The issues that led to the revocation of the institution's license included the following:

- **`bog-2019-08-16-savings-loans-revocation:L333`**
  > without a functioning board and key management personnel with the relevant qualifications and experience to conduct the business of banking.

---

## Part 2b — the rest of the section (8 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full — the extractor's vocabulary has been wrong twice already, so its judgement about what is irrelevant is not final.

- `L308` ASN Financial Services Ltd. (ASN) was licensed by the Bank of Ghana as a Finance House on July 14, 2014.
- `L317` The institution's Net worth of GHS 628,311.16 as at end May 2019, violating Section 28(1) Act 930.
- `L320` The institution's capital adequacy ratio of negative 81.39% as at end May 2019 was in violation of Section 29(2) of Act 930.
- `L323` Persistent breaches in the cash reserve ratio requirement since 2016 due to serious liquidity challenges.
- `L326` The institution has been unable to honour customer's withdrawal requests with many customer complaints received by the Bank of Ghana.
- `L330` Failure to implement Bank of Ghana on-site examination recommendations.
- `L331` Weaknesses in corporate governance practices as the institution has been
- `L335` Poor risk management culture and weak credit underwriting standards leading to high non-performing loans.

