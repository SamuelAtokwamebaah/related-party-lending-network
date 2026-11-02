# 7. Commerz Savings and Loans Limited

`inst-commerz` · notice section **L385–L414** · 3 seeded edge(s) · 7 uncited passage(s)

Read the section in `data/raw/` from L385 to L414, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1: edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E034: Commerz Savings and Loans Limited → Nordcom Africa Holdings Limited

| | |
|---|---|
| relationship | `part_of` |
| amount | not stated |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L387` |
| current decision | confirmed |

> Commerz Savings and Loans Limited (formerly known as Sterling Savings and Loans Limited and part of Nordcom Africa Holdings Limited) was licensed by the Bank of Ghana in December 2016 and commenced operations in February 2017. As a result of persistent complaints by customers that the institution was unable to meet their withdrawal request, the Bank of Ghana reviewed the operations of the institution.

*Note carried from compilation:* Holding company named in the notice. 'Formerly' may govern 'part of' as well as the name, so current membership is not certain

### P003: Commerz Savings and Loans Limited ← Nordea Capital Limited

| | |
|---|---|
| relationship | `placed_funds_with` |
| amount |  50 (ratio_only) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L1014` |
| current decision | confirmed |

> 23. NORDEA CAPITAL LIMITED Nordea Capital Limited (“Nordea”) was i ncorporated on 28th March, 2013 and licensed by the SEC as a Fund Manager on 7th May, 2013. The SEC has had a number of engagements with Nordea including Hearings pursuant to section 19 of Act 929, decisions have been issued by the SEC against Nordea with directives to take steps to comply and resolve its regulatory infractions, all to no avail. The Specific issues that led to the revocation of its licence included the following a) Failure to honour clients’ redemption request; b) Placement of client fund s with related parties without proper due diligence and the requisite standard of professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s Compliance Manual for Broker -Dealers, Investment Advisers and Representatives 2008. Placement of 50% of Funds under management with a related party; Commerz Savings and Loans (in receivership);

*Note carried from compilation:* 'Placement of 50% of Funds under management with a related party; Commerz Savings and Loans'. Commerz is one of the six institutions the Bank of Ghana did not flag for related-party exposure. The direction is into Commerz, so this does not show Commerz's own insiders extracting from it.

### P011: Commerz Savings and Loans Limited ← Mutual Integrity Asset Management Limited

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| amount |  54 (combined_total) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L974` |
| current decision | confirmed |

> 21. MUTUAL INTEGRITY ASSET MANAGEMENT LIMITED Mutual Integrity Limited (“Mutual”) was incorporated on the 1st of November, 2013 and licensed by the SEC as a Fund Manager on 15th June, 2015. The SEC has had a number of engagements with Mutual including Hearings pursuant to section 19 of Act 929, decisions have been issued by the SEC against Mutual with directives to take steps to comply and resolve its regulatory infractions, all to no avail. The Specific issues that led to the revocation of its licence included the following: a) Failure to honour clients’ redemption requests; b) Submission of inaccurate report to the SEC, contrary to section 201 of the Securities Industry Act, 2016 (Act 929); c) Payment of operational activities using client funds contrary to Section 160 of the Securities Industry Act, 2016 (Act 929); 26 d) Placement of client funds without proper due diligence and the requisite standard of professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s Compliance Manual for Broker-Dealers, Investment Advisers and Representatives 2008. 54% of placement of client funds with Commerz Savings & Loans, CDH Savings & Loans (both in receivership); and

*Note carried from compilation:* A second passage of the same notice placing client funds with Commerz; no related-party claim, so it does not bear on the related-party flag

*Amount note:* Stated as '54% of placement of client funds with Commerz Savings & Loans, CDH Savings & Loans' together. The notice gives no per-institution split.

---

## Part 2a: uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L393`**
  > The institution was found to be insolvent with an adjusted negative capital adequacy ratio with serious liquidity challenges. Bank of Ghana has since engaged the Board and Senior Management on the need to inject additional capital but that have not yielded any positive results.

---

## Part 2b: the rest of the section (6 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full, because the extractor's vocabulary has been wrong twice already and its judgement about what is irrelevant is not final.

- `L398` The specific issues that led to the revocation of its license includes the following:
- `L401` The institution's Net worth of negative GHS 40.99 million as at end May 2019 violated Section 28(1) Act 930.
- `L404` The institution's capital adequacy ratio of negative 126.15% as at end May 2019 violated Section 29(2) of Act 930.
- `L407` Serious liquidity challenges causing the inability of the institution to meet withdrawal demands of its customers.
- `L410` High and increasing non-performing loans (NPLs) ratio due to poor credit underwriting standards.
- `L413` Weaknesses in risk management oversight resulting in poor investment decisions.

