# SEC notice — sections with edges

`sec-2019-11-08-fund-manager-revocation` · 53 sections in the notice · 13 carry an edge

Each section below is reproduced in full from `data/raw/`, followed by the edges drawn from it. For each edge: does the passage support the relationship, its direction, the amount and its basis, the layer, and the confidence class? Record decisions in `data/verification.csv`.

**On the layer.** A `related_party` edge is one the Commission describes in related-party terms. A `placement` edge is a fund manager placing client money in one of the 23 with no such claim in the source. If a passage marked `placement` does state a related-party relationship, that is a finding: the edge is in the wrong layer and belongs in the headline figures.

---

## §17. STANDARD SECURITIES LIMITED (FORMERLY ASN INVESTMENTS

notice **L508–L536**

```
17. STANDARD SECURITIES LIMITED (FORMERLY ASN INVESTMENTS
     LIMITED)
Standard Securities Limited (“Standard”) was incorporated on the 2 nd of February, 2013 and licensed by
the SEC as a Fund Manager on 21st March, 2013.
The SEC has had a number of engagements with Standard including Hearings pursuant to section 19 of
Act 929, decisions have been issued by the SEC against Standard with directives to take steps to comply
and resolve its regulatory infractions, all to no avail.
The Specific issues that led to the revocation of its licence included the following:
a) Failure to honour clients’ redemption request;
b) Placement of client funds with related parties without proper due diligence and the requisite
standard of professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the
Commission’s Compliance Manual for Broker-Dealers, Investment Advisers and Representatives
2008. Related party placement with related party called ASN Financial Services Limited (in
receivership). Other Placements include Dwadifo Adanfo Microfinance (in receivership), Express
Savings & Loans (in receivership), Eclipse Microfinance (in receivership), CIG Microfinance (in
receivership) and Midland Savings & Loans (in receivership);
c) Failure to adhere to voluntary payment plans agreed on at Complaints hearings contrary to
required professional and ethical conduct in paragraph 2, 3 and 6 the SEC Compliance Manual
for Broker-Dealers, Investment Advisers and Representatives 2008 and general best international
industry practice;
15
d) Non-submission of statutory reports contrary to Regulations 33 (1) (a) (b) (c) and (6)  of L.I.
1728;
e) No evidence of a functioning board;
f) Failure to officially notify the Commission on closure of office (since August 2018) contrary to
Section 120 of the Securities Industry Act, 2016 (Act 929) and Regulation 18 of L.I. 1728; and
g) Failure to pay penalties levied by the Commission for violation of Securities Industry Laws.
```

### P001 — Standard Securities Limited → ASN Financial Services Limited

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | — |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L508` |
| current decision | **pending** |

*Note carried from compilation:* The notice says 'Related party placement with related party called ASN Financial Services Limited'. No figure is stated for it.

### P015 — Standard Securities Limited → Express Savings and Loan Limited

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| layer | `placement` |
| moves value | yes |
| amount | — |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L508` |
| current decision | **pending** |

*Note carried from compilation:* Listed under 'Other Placements', distinct from the related-party placement in the same bullet. No figure is stated.

### P016 — Standard Securities Limited → Midland Savings and Loans Company Limited

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| layer | `placement` |
| moves value | yes |
| amount | — |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L508` |
| current decision | **pending** |

*Note carried from compilation:* Listed under 'Other Placements', distinct from the related-party placement in the same bullet. No figure is stated.

---

## §4. BLACKSHIELD CAPITAL MANAGEMENT LTD (FORMERLY GOLD COAST

notice **L658–L691**

```
4.      BLACKSHIELD CAPITAL MANAGEMENT LTD (FORMERLY GOLD COAST
FUND MANAGEMENT LIMITED)
Blackshield Capital Management Ltd (formerly Gold Coa st Fund Management Limited), “Blackshield”,
was incorporated on the 12th August, 1993 prior to the passage of the Act and was licensed by the
Commission on 12th August, 2013. On 11th July, 2019, the firm changed its name to Blackshield Capital
Management Ltd.
The SEC has had a number of engagements with Blackshield including Hearings pursuant to section 19 of
Act 929, decisions have been issued by the SEC against Blackshield with directives to take steps to comply
and resolve its regulatory infractions, all to no avail.
The Specific issues that led to the revocation of its licence included the following:
a)  Failure to honour clients’ redemption requests
b) Placement of client funds with related parties without proper due diligence and the requisite
standard of professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the
Commission’s Compliance Manual for Broker -Dealers, Investment Advisers an d
Representatives 2008. According to Blackshield’s 2nd Quarter 2018 Placement Report, 99.41%
of Blackshield’s funds under management had been placed with an unregulated related entity,
Ghana Growth Fund Limited (now Gold Coast Advisors Limited).
c) Failure to adhere to voluntary payment plans agreed on at Complaints hearings contrary to
required professional and ethical conduct in paragraph 2, 3 and 6 of Part X of the SEC
Compliance Manual for Broker -Dealers, Investment Advisers and Representatives 2008 and
general best international industry practice.
d) Non-submission of statutory reports  contrary to Regulation 33 (1) (a) (b) (c) and (6)   of L.I.
1728
e) Failure to pay penalties levied by the Commission
f) Advertising of an unapproved investment product, Cardinal Ma ster Trust in contravention of
Securities Industry Act, 2016 (Act 929) and Securities and Exchange Commission Regulations,
2003 (LI 1728).
19
```

### S014 — Gold Coast Fund Management Limited → Ghana Growth Fund

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | 99.41% (ratio_only) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L658` |
| current decision | pending |

*Amount note:* 99.41% of funds under management; a ratio, not an amount

*Note carried from compilation:* Both are named in the BoG notice as sister companies of GN; this documents the link between them

---

## §7. CORPORATE HILLS INVESTMENT LTD.

notice **L722–L745**

```
7. CORPORATE HILLS INVESTMENT LTD.
Corporate Hills Investment Limited (“Corporate Hills”) was incorporated on the 7th of April, 2014 and was
licensed by the SEC as a Fund Manager on 9th December, 2014.
The SEC has had a number of engagements with Corporate Hills including Hearings pursuant to section
19 of Act 929, decisions have been issued by the SEC against Corporate Hills with directives to take steps
to comply and resolve its regulatory infractions, all to no avail.
The Specific issues that led to the revocation of its licence included the following:
a) Failure to honour clients’ redemption requests;
20
b) Placement of client funds without due diligence and the requisite standard of professional conduct
contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s Compliance Manual for
Broker-Dealers, Investment Advisers and Representatives 2008. Placements include 54.19% of its
assets under management with ASN Financial Services Ltd. (in receivership) and 35.98% in a
commercial paper issued by Samba Transfer Services (a breach of the Guidelines on Comme rcial
Paper issued by the Commission);
c) Failure to prepare bank reconciliation of all accounts (Part V section L (5a) of the SEC Compliance
Manual);
d) Failure to adhere to voluntary payment plans agreed on at Complaints hearings contrary to required
professional and ethical conduct in paragraph 2, 3 and 6 the SEC Compliance Manual for Broker-
Dealers, Investment Advisers and Representatives 2008 and general best international industry
practice;
e) Failure to conduct regular board meetings (Section 188(1) of the Companies Act, 2019 (Act 992).
```

### P004 — Corporate Hills Investment Limited → ASN Financial Services Limited

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| layer | `placement` |
| moves value | yes |
| amount | 54.19% (ratio_only) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L722` |
| current decision | **pending** |

---

## §13. GOLDSTREET FUND MANAGEMENT LIMITED (FORMERLY GOLDSTREET

notice **L835–L858**

```
13.  GOLDSTREET FUND MANAGEMENT LIMITED (FORMERLY GOLDSTREET
INVESTMENTS LTD)
Goldstreet Fund Management Limited (“Goldstreet”) was incorporated on the 17th December, 2014. It was
licensed by the SEC as a Fund Manager on 29th September, 2015.
The SEC has had a number of engagements with Goldstreet including Hearings pursuant to section 19 of
Act 929, decisions have been issued by the SEC against Goldstreet with directives to take steps to comply
and resolve its regulatory infractions, all to no avail.
The Specific issues that led to the revocation of its licence included the following
a) Failure to honour clients’ redemption requests;
b) Payment of operational activities using client funds contrary to Section 160 of the Act 929;
c) Non submission of statutory reports contrary to Regulations 33 (1) (a) (b) (c ) and (6) of LI
1728
d) Placement of client funds with out proper due diligence and the requisite standard of
professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s
Compliance Manual for Broker -Dealers, Investment Advisers and Representatives 2008.
Placements include 50.61% with Ideal Finance Ltd ( in receivership) and  10.06% with First
Trust Savings & Loans (in receivership)
23
```

### P005 — Goldstreet Fund Management Limited → Ideal Finance Limited

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| layer | `placement` |
| moves value | yes |
| amount | 50.61% (ratio_only) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L835` |
| current decision | **pending** |

### P006 — Goldstreet Fund Management Limited → FirsTrust Savings and Loans Limited

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| layer | `placement` |
| moves value | yes |
| amount | 10.06% (ratio_only) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L835` |
| current decision | **pending** |

---

## §14. IDEAL CAPITAL PARTNERS LIMITED

notice **L859–L874**

```
14. IDEAL CAPITAL PARTNERS LIMITED
Ideal Capital Partners Limited (“Ideal”) was incorporated on the 21st July 2011. It was licensed by the SEC
as a Fund Manager on 18th June, 2014.
The SEC has had a number of engagements with Ideal including Hearings pursuant to section 19 of Act
929, decisions have been issued by the SEC against Ideal with directives to take steps to comply and resolve
its regulatory infractions, all to no avail.
The Specific issues that led to the revocation of its licence included the following
a) Failure to honour clients’ redemption requests;
b) Placement of client funds without proper due diligence and the requisite standard of
professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s
Compliance Manual for Broker-Dealers, Investment Advisers and Representatives 2008. The
firm had 19% of AUM in related parties (Ideal Financial Holdings Ltd, Firstrust Savings and
Loans, Ideal Trade Limited, Ideal Bottling Limited) and over 48% of funds placed in illiquid
instruments.
c) Failure to adhere to voluntary payment plans agreed on at Complaints hearings
```

### S001 — Ideal Capital Partners → Ideal Financial Holdings

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | 19% (combined_total) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L859` |
| current decision | pending |

*Amount note:* Stated as '19% of AUM in related parties' across Ideal Financial Holdings, FirsTrust, Ideal Trade and Ideal Bottling together. No per-counterparty split is given.

*Note carried from compilation:* SEC records Ideal Financial Holdings as a related party of Ideal Capital Partners

### S002 — Ideal Capital Partners → FirsTrust Savings and Loans Limited

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | 19% (combined_total) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L859` |
| current decision | pending |

*Amount note:* Stated as '19% of AUM in related parties' across Ideal Financial Holdings, FirsTrust, Ideal Trade and Ideal Bottling together. No per-counterparty split is given.

*Note carried from compilation:* The link that connects one counterparty to two of the 23; source spells FirsTrust as Firstrust

### S003 — Ideal Capital Partners → Ideal Trade Limited

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | 19% (combined_total) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L859` |
| current decision | pending |

*Amount note:* Stated as '19% of AUM in related parties' across Ideal Financial Holdings, FirsTrust, Ideal Trade and Ideal Bottling together. No per-counterparty split is given.

*Note carried from compilation:* Non-financial group company

### S004 — Ideal Capital Partners → Ideal Bottling Limited

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | 19% (combined_total) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L859` |
| current decision | pending |

*Amount note:* Stated as '19% of AUM in related parties' across Ideal Financial Holdings, FirsTrust, Ideal Trade and Ideal Bottling together. No per-counterparty split is given.

*Note carried from compilation:* Non-financial group company

---

## §15. INTEGRITY FUND MANAGEMENT LTD

notice **L875–L885**

```
15. INTEGRITY FUND MANAGEMENT LTD
Integrity Fund Management Ltd (“Integrity”) was incorporated on 22nd August, 2015 and licensed as a Fund
Manager on 10th December, 2015.
The SEC has directed Integrity to resolve its regulatory infractions, all to no avail.
The Specific issue that led to the revocation of its licence was the following:
a)  Placement of client funds  without proper due diligence and the requisite standard of professional
conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s Compliance Manual
for Broker-Dealers, Investment Advisers and Representatives 2008. Over 80% placement of client
funds in revoked savings & loans including, Midland S avings & Loans, First Trust Savings &
Loans and Legacy Savings & Loans.
```

### P007 — Integrity Fund Management Ltd → Midland Savings and Loans Company Limited

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| layer | `placement` |
| moves value | yes |
| amount | 80% (combined_total) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L875` |
| current decision | **pending** |

*Amount note:* Stated as 'Over 80% placement of client funds in revoked savings & loans' across Midland, FirsTrust and Legacy Capital together. The notice gives no per-institution split, and the figure is a floor.

### P008 — Integrity Fund Management Ltd → FirsTrust Savings and Loans Limited

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| layer | `placement` |
| moves value | yes |
| amount | 80% (combined_total) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L875` |
| current decision | **pending** |

*Amount note:* Stated as 'Over 80% placement of client funds in revoked savings & loans' across Midland, FirsTrust and Legacy Capital together. The notice gives no per-institution split, and the figure is a floor.

### P009 — Integrity Fund Management Ltd → Legacy Capital Savings and Loans Ltd.

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| layer | `placement` |
| moves value | yes |
| amount | 80% (combined_total) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L875` |
| current decision | **pending** |

*Amount note:* Stated as 'Over 80% placement of client funds in revoked savings & loans' across Midland, FirsTrust and Legacy Capital together. The notice gives no per-institution split, and the figure is a floor.

---

## §18. LEGACY FUND MANAGEMENT LIMITED

notice **L919–L944**

```
18. LEGACY FUND MANAGEMENT LIMITED
(FORMERLY LEGACY FINANCIAL SERVICES LTD)
Legacy Fund Management Limited (“Legacy”) was incorporated on the 23rd July 2013 and licensed by the
SEC as a Fund Manager on 18thJune, 2014.
The SEC has had a number of engagements with Legacy including Hearings pursuant to section 19 of Act
929, decisions have been issued by the SEC against Legacy with directives to take steps to comply and
resolve its regulatory infractions, all to no avail.
The Specific issues that led to the revocation of its licence included the following
a) Failure to honour clients’ redemption requests;
b) Placement of client funds with related parties without proper due diligence and the requisite
standard of professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the
Commission’s Compliance Manual for Broker-Dealers, Investment Advisers and Representatives
2008. Placement of 18% of funds in related party Legacy Capital Savings Limited (in receivership)
and 33% of funds with other Fund Managers (23% with Firstbanc Financial Services);
c) Operating an unlicensed CIS product contrary to Section 109 (1) (2) of Act 929;
d)  Payment of operational activities using client funds contrary to Section 160 of the Act 929; and
e) Failure to adhere to voluntary payment plans agreed on at Complaints hearings contrary to required
professional and ethical conduct in paragraph 2, 3 and 6 the SEC Compliance Manual for Broker-
Dealers, Investment Advisers and Representatives 2008 and gene ral best international industry
practice.
25
```

### P002 — Legacy Fund Management Limited → Legacy Capital Savings and Loans Ltd.

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | 18% (ratio_only) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L919` |
| current decision | **pending** |

*Note carried from compilation:* 'Placement of 18% of funds in related party Legacy Capital Savings Limited'. Settles resolution candidate RR006: the Commission states the relationship, so it no longer rests on a shared name.

---

## §19. LIBERTY ASSET MANAGEMENT LIMITED.

notice **L945–L963**

```
19.    LIBERTY ASSET MANAGEMENT LIMITED.
Liberty Asset Management Limited (“Liberty”) was licensed by the SEC as a Fund Manager on 15th April,
2008.
The SEC has had a number of engagements with Liberty including Hearings pursuant to section 19 of Act
929, decisions have been issued by the SEC against Liberty with directives to take steps to comply and
resolve its regulatory infractions, all to no avail.
a) Failure to honour clients’ redemption request;
b) Placement of client funds with related parties due diligence and the requisite standard of
professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s
Compliance Manual for Broker-Dealers, Investment Advisers and Representatives 2008. The
firm had 9.45 % of its funds with Midland Savings & Loans Limited (in receivership) and
10.93% in Liberty Commodities Limited (both are related parties);
c) Failure to monitor liquidity levels and introduce capital contrary to Regulations 22 and 23 of
L.I 1728; and
d) Failure to adhere to voluntary payment plans agreed on at Complaints hearings contrary to
required professional and ethical conduct in paragraph 2, 3 and 6 the SEC Compliance Manual
for B roker-Dealers, Investment Advisers and Representatives 2008 and general best
international industry practice.
```

### S005 — Liberty Asset Management → Midland Savings and Loans Company Limited

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | 9.45% (ratio_only) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L945` |
| current decision | pending |

*Amount note:* 9.45% of funds under management; a ratio, not an amount

*Note carried from compilation:* Midland was over-exposed to Liberty and Liberty held funds with Midland: each held the other

### S006 — Liberty Asset Management → Liberty Commodities Limited

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | 10.93% (ratio_only) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L945` |
| current decision | pending |

*Amount note:* 10.93% of funds under management; a ratio, not an amount

---

## §20. MONARCH CAPITAL LIMITED

notice **L964–L973**

```
20. MONARCH CAPITAL LIMITED
Monarch Capital Ltd (“Monarch”) was incorporated on 24 th March, 2013 and was licensed by the SEC as
a Fund Manager on 29th December, 2015.
The SEC has directed Monarch to resolve its regulatory infractions, all to no avail.
The Specific issue that led to the revocation of its licence included the following:
a) Placement of client funds without proper due diligence and the requisite standard of professional
conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s Compliance Manual
for Broker-Dealers, Investment Advisers and Representatives 2008. The firm placed 78% of client
funds with Legacy Capital Savings & Loans (in receivership).
```

### P010 — Monarch Capital Limited → Legacy Capital Savings and Loans Ltd.

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| layer | `placement` |
| moves value | yes |
| amount | 78% (ratio_only) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L964` |
| current decision | **pending** |

---

## §21. MUTUAL INTEGRITY ASSET MANAGEMENT LIMITED

notice **L974–L996**

```
21. MUTUAL INTEGRITY ASSET MANAGEMENT LIMITED
Mutual Integrity Limited (“Mutual”) was incorporated on the 1st of November, 2013 and licensed by the
SEC as a Fund Manager on 15th June, 2015.
The SEC has had a number of engagements with Mutual including Hearings pursuant to section 19 of Act
929, decisions have been issued by the SEC against Mutual with directives to take steps to comply and
resolve its regulatory infractions, all to no avail.
The Specific issues that led to the revocation of its licence included the following:
a) Failure to honour clients’ redemption requests;
b) Submission of inaccurate report to the SEC, contrary to section 201 of the Securities Industry Act,
2016 (Act 929);
c) Payment of operational activities using client funds contrary to Section 160 of the Securities
Industry Act, 2016 (Act 929);
26
d) Placement of client funds without proper due diligence and the requisite standard of professional
conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s Compliance Manual
for Broker-Dealers, Investment Advisers and Representatives 2008. 54% of placement of client
funds with Commerz Savings & Loans, CDH Savings & Loans (both in receivership); and
e) Failure to adhere to voluntary payment plans agreed on at Complaints hearings contrary to required
professional and ethical conduct in paragraph 2, 3 and 6 of Part X of the SEC Compliance Manual
for Broker-Dealers, Investment Advisers and Representatives 2008 and general best i nternational
industry practice.
```

### P011 — Mutual Integrity Asset Management Limited → Commerz Savings and Loans Limited

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| layer | `placement` |
| moves value | yes |
| amount | 54% (combined_total) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L974` |
| current decision | **pending** |

*Amount note:* Stated as '54% of placement of client funds with Commerz Savings & Loans, CDH Savings & Loans' together. The notice gives no per-institution split.

*Note carried from compilation:* The second document to put Commerz on the receiving end of a placement, and the second reason the six unflagged institutions are unflagged only in the Bank of Ghana notice.

### P012 — Mutual Integrity Asset Management Limited → CDH Savings and Loans Ltd.

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| layer | `placement` |
| moves value | yes |
| amount | 54% (combined_total) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L974` |
| current decision | **pending** |

*Amount note:* Stated as '54% of placement of client funds with Commerz Savings & Loans, CDH Savings & Loans' together. The notice gives no per-institution split.

---

## §23. NORDEA CAPITAL LIMITED

notice **L1014–L1035**

```
23. NORDEA CAPITAL LIMITED
Nordea Capital Limited (“Nordea”) was i ncorporated on 28th March, 2013 and  licensed by the SEC as a
Fund Manager on 7th May, 2013.
The SEC has had a number of engagements with Nordea including Hearings pursuant to section 19 of Act
929, decisions have been issued by the SEC against Nordea  with directives to take steps to comply and
resolve its regulatory infractions, all to no avail.
The Specific issues that led to the revocation of its licence included the following
a) Failure to honour clients’ redemption request;
b) Placement of client fund s with related parties without proper due diligence and the requisite
standard of professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the
Commission’s Compliance Manual for Broker -Dealers, Investment Advisers and
Representatives 2008. Placement of 50% of Funds under management with a related party;
Commerz Savings and Loans  (in receivership);
c) Failure to monitor liquidity levels and introduce capital contrary to Regulations 22 and 23   of
L.I 1728; and
27
d) Failure to adhere to voluntary pay ment plans agreed on at Complaints hearings contrary to
required professional and ethical conduct in paragraph 2, 3 and 6 the SEC Compliance Manual
for Broker -Dealers, Investment Advisers and Representatives 2008 and general best
international industry practice.
```

### P003 — Nordea Capital Limited → Commerz Savings and Loans Limited

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | 50% (ratio_only) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L1014` |
| current decision | **pending** |

*Note carried from compilation:* 'Placement of 50% of Funds under management with a related party; Commerz Savings and Loans'. Commerz is one of the six institutions the Bank of Ghana did not flag for related-party exposure. The direction is into Commerz, so this does not show Commerz's own insiders extracting from it.

---

## §25. PROCAP FINANCE LIMITED

notice **L1054–L1064**

```
25. PROCAP FINANCE LIMITED
Procap Finance Ltd (“Procap”) was incorporated on 13 th June, 2016 and licensed by the SEC on a 4th
December 2017 as a Fund Manager.
The SEC has directed Procap to resolve its regulatory infractions, all to no avail.
The Specific issue that led to the revocation of its licence:
a) Placement of client funds without proper due diligence and the requisite standard of professional
conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s Compliance Manual
for Broker -Dealers, Investment Advisers and Representatives 200 8. Over 68% placement in
revoked Savings and Loans institutions including Midland Savings and Loans and FirsTrust
Savings & Loans .
```

### P013 — Procap Finance Limited → Midland Savings and Loans Company Limited

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| layer | `placement` |
| moves value | yes |
| amount | 68% (combined_total) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L1054` |
| current decision | **pending** |

*Amount note:* Stated as 'Over 68% placement in revoked Savings and Loans institutions including Midland Savings and Loans and FirsTrust' together. The notice gives no per-institution split, the figure is a floor, and 'including' leaves the list open.

### P014 — Procap Finance Limited → FirsTrust Savings and Loans Limited

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| layer | `placement` |
| moves value | yes |
| amount | 68% (combined_total) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L1054` |
| current decision | **pending** |

*Amount note:* Stated as 'Over 68% placement in revoked Savings and Loans institutions including Midland Savings and Loans and FirsTrust' together. The notice gives no per-institution split, the figure is a floor, and 'including' leaves the list open.

---

## §30. UNISECURITIES (GHANA) LTD.

notice **L1140–L1158**

```
30.  UNISECURITIES (GHANA) LTD.
Unisecurities (Ghana) Limited (“Unisecurities”) was incorporated on 29 th March, 2010 and was licensed
by the SEC as a Fund Manager on 8th October, 2010.
The SEC has had a number of engagements with Unisecurities including Hearings pursuant to section 19
of Act 929 , decisions have been issued by the SEC against Unisecurities with directives to take steps to
comply and resolve its regulatory infractions, all to no avail.
The Specific issues that led to the revocation of its licence included the following:
a) Failure to honour clients’ redemption request;
b) Placement of client funds without proper due diligence and the requisite standard of professional
conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s Compliance Manual
for Broker-Dealers, Investment Advisers and Representatives 2008. Related parties Hoda Holdings
Ltd , Intrepid Venture Capital Ltd, Premier Portfolio, Integrated Properties Ltd, Bolton Portfolio
Ltd, Numa Logistics and Alban logistics
c) Failure to adhere to voluntary payment plans agreed on at Complaints hearings contrary to required
professional and ethical conduct in paragraph 2, 3 and 6 the SEC Compliance Manual for Broker-
Dealers, Investment Advisers and Representatives 2008 and general best internat ional industry
practice.
30
```

### S007 — uniSecurities Limited → Hoda Holdings Ltd

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | — |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L1140` |
| current decision | pending |

*Note carried from compilation:* Whether Hoda Holdings Ltd is the Hoda Group of Companies that acquired uniCredit is undecided; see RR004

### S008 — uniSecurities Limited → Intrepid Venture Capital Ltd

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | — |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L1140` |
| current decision | pending |

### S009 — uniSecurities Limited → Premier Portfolio

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | — |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L1140` |
| current decision | pending |

### S010 — uniSecurities Limited → Integrated Properties Ltd

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | — |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L1140` |
| current decision | pending |

### S011 — uniSecurities Limited → Bolton Portfolio Ltd

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | — |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L1140` |
| current decision | pending |

### S012 — uniSecurities Limited → Numa Logistics

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | — |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L1140` |
| current decision | pending |

### S013 — uniSecurities Limited → Alban Logistics

| | |
|---|---|
| relationship | `placed_funds_with` |
| layer | `related_party` |
| moves value | yes |
| amount | — |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L1140` |
| current decision | pending |

---

