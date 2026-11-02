# 19. Legacy Capital Savings and Loans Ltd.

`inst-legacy-capital` · notice section **L1005–L1039** · 4 seeded edge(s) · 8 uncited passage(s)

Read the section in `data/raw/` from L1005 to L1039, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1: edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E027: Legacy Capital Savings and Loans Ltd. → UNNAMED related parties of Legacy Capital

| | |
|---|---|
| relationship | `over_exposed_to` |
| amount | GHS 4.49m (exact) |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L1027` |
| current decision | confirmed |

> Non-performing related party exposures of GHS 4.49 million constituted 200% of the institution's reported net own funds in breach of Act 930.

*Note carried from compilation:* Amount stated; names not

### P002: Legacy Capital Savings and Loans Ltd. ← Legacy Fund Management Limited

| | |
|---|---|
| relationship | `placed_funds_with` |
| amount |  18 (ratio_only) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L919` |
| current decision | confirmed |

> 18. LEGACY FUND MANAGEMENT LIMITED (FORMERLY LEGACY FINANCIAL SERVICES LTD) Legacy Fund Management Limited (“Legacy”) was incorporated on the 23rd July 2013 and licensed by the SEC as a Fund Manager on 18thJune, 2014. The SEC has had a number of engagements with Legacy including Hearings pursuant to section 19 of Act 929, decisions have been issued by the SEC against Legacy with directives to take steps to comply and resolve its regulatory infractions, all to no avail. The Specific issues that led to the revocation of its licence included the following a) Failure to honour clients’ redemption requests; b) Placement of client funds with related parties without proper due diligence and the requisite standard of professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s Compliance Manual for Broker-Dealers, Investment Advisers and Representatives 2008. Placement of 18% of funds in related party Legacy Capital Savings Limited (in receivership) and 33% of funds with other Fund Managers (23% with Firstbanc Financial Services);

*Note carried from compilation:* 'Placement of 18% of funds in related party Legacy Capital Savings Limited'. Settles resolution candidate RR006: the Commission states the relationship, so it no longer rests on a shared name.

### P009: Legacy Capital Savings and Loans Ltd. ← Integrity Fund Management Ltd

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| amount |  80 (combined_total) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L875` |
| current decision | confirmed |

> 15. INTEGRITY FUND MANAGEMENT LTD Integrity Fund Management Ltd (“Integrity”) was incorporated on 22nd August, 2015 and licensed as a Fund Manager on 10th December, 2015. The SEC has directed Integrity to resolve its regulatory infractions, all to no avail. The Specific issue that led to the revocation of its licence was the following: a) Placement of client funds without proper due diligence and the requisite standard of professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s Compliance Manual for Broker-Dealers, Investment Advisers and Representatives 2008. Over 80% placement of client funds in revoked savings & loans including, Midland S avings & Loans, First Trust Savings & Loans and Legacy Savings & Loans.

*Amount note:* Stated as 'Over 80% placement of client funds in revoked savings & loans including' Midland, FirsTrust and Legacy Capital. The notice gives no per-institution split, the figure is a floor, and 'including' leaves the list open.

### P010: Legacy Capital Savings and Loans Ltd. ← Monarch Capital Limited

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| amount |  78 (ratio_only) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L964` |
| current decision | confirmed |

> 20. MONARCH CAPITAL LIMITED Monarch Capital Ltd (“Monarch”) was incorporated on 24 th March, 2013 and was licensed by the SEC as a Fund Manager on 29th December, 2015. The SEC has directed Monarch to resolve its regulatory infractions, all to no avail. The Specific issue that led to the revocation of its licence included the following: a) Placement of client funds without proper due diligence and the requisite standard of professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s Compliance Manual for Broker-Dealers, Investment Advisers and Representatives 2008. The firm placed 78% of client funds with Legacy Capital Savings & Loans (in receivership).

---

## Part 2a: uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L1012`**
  > The institution was found to be facing liquidity challenges in August 2018. A subsequent assessment indicated that the institution was insolvent and also facing serious liquidity challenges. The institution's adjusted capital adequacy ratio was negative as at end-May 2019. The Bank of Ghana has since August, 2018 engaged the Board and Senior Management on the need to inject additional capital.

---

## Part 2b: the rest of the section (7 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full, because the extractor's vocabulary has been wrong twice already and its judgement about what is irrelevant is not final.

- `L1007` Legacy Capital Savings & Loans Company Limited (LCSL) was licensed by Bank of Ghana to operate as a savings and loans company on August 12, 2016, afte …
- `L1018` The specific issues that led to the revocation of its license included the following:
- `L1020` The institution's adjusted Net worth of negative GHS 19.52 million as at end May 2019 indicates that its paid up capital is impaired in violation of S …
- `L1024` The institution's adjusted capital adequacy ratio of negative 16.96% as at end May 2019 is in violation of Section 29(2) of Act 930.
- `L1031` The institution has consistently breached the minimum cash reserve ratio requirement since August 2018 due to liquidity challenges. The cash reserve r …
- `L1035` The institution failed to keep accounting records in a manner that gives an accurate and reliable account of its transactions.
- `L1038` Poor loan underwriting standards resulting in the impairment of loans.

