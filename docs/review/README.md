# Verification pack

One sheet per institution. Each pairs the edges seeded against it with the passages they came from, and lists every passage in that section that no edge cites.

The seeded rows were a first pass built by script from the Phase 0 candidate sheet. An edge counts as verified only once it carries a decision in `data/verification.csv`; the loader reports how many do on every build.

Decisions: `confirmed`, `corrected`, `rejected`, `pending`.

Work the sheets with a non-zero **To check** count first: those sections contain a passage carrying relationship wording that no edge cites.

| # | Institution | Sheet | Edges | To check | Rest |
|---|---|---|---|---|---|
| 1 | Accent Financial Services Limited | [01-accent-financial-services.md](01-accent-financial-services.md) | 1 | **2** | 9 |
| 2 | Adom Savings and Loans Limited | [02-adom-savings-and-loans.md](02-adom-savings-and-loans.md) | 2 | **2** | 8 |
| 3 | AllTime Finance Limited | [03-alltime-finance.md](03-alltime-finance.md) | 2 | **1** | 10 |
| 4 | Alpha Capital Savings and Loans Ltd. | [04-alpha-capital-savings-and-loans.md](04-alpha-capital-savings-and-loans.md) | 0 | **2** | 6 |
| 5 | ASN Financial Services Limited | [05-asn-financial-services.md](05-asn-financial-services.md) | 3 | **2** | 8 |
| 6 | CDH Savings and Loans Ltd. | [06-cdh-savings-and-loans.md](06-cdh-savings-and-loans.md) | 5 | **1** | 4 |
| 7 | Commerz Savings and Loans Limited | [07-commerz-savings-and-loans.md](07-commerz-savings-and-loans.md) | 3 | **1** | 6 |
| 8 | Crest Finance House Limited | [08-crest-finance-house.md](08-crest-finance-house.md) | 3 | **2** | 9 |
| 9 | Dream Finance Limited | [09-dream-finance.md](09-dream-finance.md) | 2 | **2** | 9 |
| 10 | Express Savings and Loan Limited | [10-express-savings-and-loan.md](10-express-savings-and-loan.md) | 2 | **1** | 9 |
| 11 | First Allied Savings and Loans Limited | [11-first-allied-savings-and-loans.md](11-first-allied-savings-and-loans.md) | 2 | 0 | 11 |
| 12 | First African Savings and Loans Limited | [12-first-african-savings-and-loans.md](12-first-african-savings-and-loans.md) | 2 | **1** | 7 |
| 13 | First Ghana Savings and Loans Limited | [13-first-ghana-savings-and-loans.md](13-first-ghana-savings-and-loans.md) | 0 | **1** | 3 |
| 14 | FirsTrust Savings and Loans Limited | [14-firstrust-savings-and-loans.md](14-firstrust-savings-and-loans.md) | 9 | **2** | 6 |
| 15 | Global Access Savings and Loans Company Limited | [15-global-access-savings-and-loans-company.md](15-global-access-savings-and-loans-company.md) | 2 | **1** | 9 |
| 16 | GN Savings and Loans Ltd. | [16-gn-savings-and-loans.md](16-gn-savings-and-loans.md) | 6 | **3** | 7 |
| 17 | Ideal Finance Limited | [17-ideal-finance.md](17-ideal-finance.md) | 6 | **5** | 15 |
| 18 | IFS Financial Services Limited | [18-ifs-financial-services.md](18-ifs-financial-services.md) | 0 | **1** | 8 |
| 19 | Legacy Capital Savings and Loans Ltd. | [19-legacy-capital-savings-and-loans.md](19-legacy-capital-savings-and-loans.md) | 4 | **1** | 7 |
| 20 | Midland Savings and Loans Company Limited | [20-midland-savings-and-loans-company.md](20-midland-savings-and-loans-company.md) | 7 | **1** | 9 |
| 21 | Sterling Financial Services Limited | [21-sterling-financial-services.md](21-sterling-financial-services.md) | 0 | **1** | 1 |
| 22 | uniCredit Ghana Limited | [22-unicredit-ghana.md](22-unicredit-ghana.md) | 2 | **1** | 5 |
| 23 | Women's World Banking Ghana (WWBG) Savings and Loans Limited | [23-women-s-world-banking-ghana-wwbg-savings-and-loa.md](23-women-s-world-banking-ghana-wwbg-savings-and-loa.md) | 0 | **1** | 8 |

**Totals:** 63 edge listings (an edge touching two institutions is listed on both sheets), 35 uncited passages carrying relationship wording, 174 other passages, across 23 institutions.

Regenerate with `python scripts/build_review_pack.py`. It rewrites the sheets and adds rows to `data/verification.csv` for any new edge, but never overwrites a decision already recorded there.

## The other notice

These sheets are built from the sections of the Bank of Ghana notice. They also list any Securities and Exchange Commission or court edge touching the institution, but the Commission's notice is arranged by fund manager rather than by institution, so its own pack is built separately and lives in [sec/](sec/). The Court of Appeal judgment on GN has a sheet of its own, [ca-2026-05-21-gn-judgment.md](ca-2026-05-21-gn-judgment.md). Two edges touch no institution and so appear on no sheet here: E043, whose passage is shown on the GN sheet beside E042, and the inferred I002.

- [sec/01-sections-with-edges.md](sec/01-sections-with-edges.md): every section an edge cites, reproduced in full, with the edges drawn from it
- [sec/02-coverage.md](sec/02-coverage.md): every section, marked for whether they name one of the 23 and whether an edge exists. Read this one first: v0.3 read four sections and stopped, and nine more named one of the 23.

Regenerate with `python scripts/build_sec_review.py`.
