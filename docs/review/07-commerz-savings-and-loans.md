# 7. Commerz Savings and Loans Limited

`inst-commerz` · notice section **L385–L414** · 1 seeded edge(s) · 7 uncited passage(s)

Read the section in `data/raw/` from L385 to L414, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1 — edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E034 — Commerz Savings and Loans Limited → Nordcom Africa Holdings Limited

| | |
|---|---|
| relationship | `part_of` |
| amount | — |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L387` |
| current decision | pending |

> Commerz Savings and Loans Limited (formerly known as Sterling Savings and Loans Limited and part of Nordcom Africa Holdings Limited) was licensed by the Bank of Ghana in December 2016 and commenced operations in February 2017. As a result of persistent complaints by customers that the institution was unable to meet their withdrawal request, the Bank of Ghana reviewed the operations of the institution.

*Note carried from compilation:* Holding company named in the notice

---

## Part 2a — uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L393`**
  > The institution was found to be insolvent with an adjusted negative capital adequacy ratio with serious liquidity challenges. Bank of Ghana has since engaged the Board and Senior Management on the need to inject additional capital but that have not yielded any positive results.

---

## Part 2b — the rest of the section (6 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full — the extractor's vocabulary has been wrong twice already, so its judgement about what is irrelevant is not final.

- `L398` The specific issues that led to the revocation of its license includes the following:
- `L401` The institution's Net worth of negative GHS 40.99 million as at end May 2019 violated Section 28(1) Act 930.
- `L404` The institution's capital adequacy ratio of negative 126.15% as at end May 2019 violated Section 29(2) of Act 930.
- `L407` Serious liquidity challenges causing the inability of the institution to meet withdrawal demands of its customers.
- `L410` High and increasing non-performing loans (NPLs) ratio due to poor credit underwriting standards.
- `L413` Weaknesses in risk management oversight resulting in poor investment decisions.

