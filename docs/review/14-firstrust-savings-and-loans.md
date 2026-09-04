# 14. FirsTrust Savings and Loans Limited

`inst-firstrust` · notice section **L657–L712** · 5 seeded edge(s) · 8 uncited passage(s)

Read the section in `data/raw/` from L657 to L712, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1 — edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E017 — FirsTrust Savings and Loans Limited → UNNAMED six related companies of FirsTrust

| | |
|---|---|
| relationship | `over_exposed_to` |
| amount | GHS 17.93m (exact) |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L685` |
| current decision | confirmed |

> The use of depositors' funds to finance related party projects. The institution is over exposed to six (6) of its related companies to the tune of GHS 17.93 million. The non-performing related party exposures, has contributed significantly to the liquidity challenges of the institution.

*Note carried from compilation:* Count and amount stated; names not

### E018 — FirsTrust Savings and Loans Limited → Ideal Finance Limited

| | |
|---|---|
| relationship | `proposed_merger_with` |
| amount | GHS 127.00m (exact) |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L702` |
| current decision | confirmed |

> Bank of Gnana declined a request dated 25th July, 2019 to merge the operations of FirsTrust Savings and Loans Limited and Ideal Finance Limited because the two institutions under consideration are both insolvent and illiquid. The total projected cash injection of GHS 127.00 million, if approved, will lead to total shareholders' funds of the proposed merged entity from negative GHS 291.60 million to negative GHS 164.60 million and CAR from negative 78.32% to negative 47.26% leaving a significant capital deficit of GHS 234.05 million. The merger was therefore, not going to address the current financial challenges facing the two institutions, or improve their future prospects.

*Note carried from compilation:* Institution-to-institution link

*Amount note:* projected cash injection for the proposed merger, not an exposure

### E024 — FirsTrust Savings and Loans Limited ← Ideal Finance Limited

| | |
|---|---|
| relationship | `related_party_exposure_to` |
| amount | — |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L894` |
| current decision | confirmed |

> Contrary to section 64 (2) of the Banks and Specialised Deposit-Taking Institutions Act, 2016 (Act 930), the institution's exposure to its related party has consistently been above the regulatory limit of 25% of net own funds (NOF). Exposures to related parties (FirstTrust Savings & Loans and Ideal Capital partners) were to the tune of Ghc63.19 million.

*Note carried from compilation:* Combined total GHS 63.19m across E024 and E025; source spells FirsTrust as FirstTrust

*Amount note:* GHS 63.19m is stated across E024 and E025 together

### E037 — FirsTrust Savings and Loans Limited ← Ideal Financial Holdings

| | |
|---|---|
| relationship | `acquired` |
| amount | — |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L659` |
| current decision | confirmed |

> FirsTrust Savings and Loans Company Limited (FTSL) was authorised as a savings and loans by the Bank of Ghana on September 19, 2014 and was issued a license as FTSL on January 28, 2015. The name was changed to FirstTrust in January 2015. . Prior to this, the institution was known as EZI Savings and Loans (EZI) Limited which was licensed by the BOG as a savings and loans institution on October 11, 2007 until its acquisition by Ideal Financial Holdings in 2014.

*Note carried from compilation:* Acquisition dated 2014

### S002 — FirsTrust Savings and Loans Limited ← Ideal Capital Partners

| | |
|---|---|
| relationship | `placed_funds_with` |
| amount | — |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L859` |
| current decision | pending |

> 14. IDEAL CAPITAL PARTNERS LIMITED Ideal Capital Partners Limited (“Ideal”) was incorporated on the 21st July 2011. It was licensed by the SEC as a Fund Manager on 18th June, 2014. The SEC has had a number of engagements with Ideal including Hearings pursuant to section 19 of Act 929, decisions have been issued by the SEC against Ideal with directives to take steps to comply and resolve its regulatory infractions, all to no avail. The Specific issues that led to the revocation of its licence included the following a) Failure to honour clients’ redemption requests; b) Placement of client funds without proper due diligence and the requisite standard of professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s Compliance Manual for Broker-Dealers, Investment Advisers and Representatives 2008. The firm had 19% of AUM in related parties (Ideal Financial Holdings Ltd, Firstrust Savings and Loans, Ideal Trade Limited, Ideal Bottling Limited) and over 48% of funds placed in illiquid instruments.

*Note carried from compilation:* The link that connects one counterparty to two of the 23; source spells FirsTrust as Firstrust

*Amount note:* 19% of assets under management across the four related parties named

---

## Part 2a — uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L670`**
  > The Bank of Ghana engaged the Board and Senior Management on the need to inject additional capital. The specific issues that led to the revocation of its license included the following:

- **`bog-2019-08-16-savings-loans-revocation:L691`**
  > Weaknesses in corporate governance practices as the institution is without a functioning board since August 2018.

---

## Part 2b — the rest of the section (6 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full — the extractor's vocabulary has been wrong twice already, so its judgement about what is irrelevant is not final.

- `L666` Bank of Ghana's reviews conducted in 2015, 2016 and 2017 all showed that the institution was showing severe signs of distress. The institution reporte …
- `L674` The institution's Net worth of negative GHS 175.90 million as at end May 2019 indicates that its paid up capital is impaired in violation of Section 2 …
- `L677` The institution's capital adequacy ratio of negative 132.96% as at end May 2019 is in violation of Section 29(2) of Act 930.
- `L680` The institution has breached the statutory cash reserve ratio (CRR) requirement since January 2018. The institution is currently facing challenges in  …
- `L694` The institution has consistently failed to implement Bank of Ghana on-site examination recommendations including the payment of penalties imposed for  …
- `L698` The institution failed to keep accounting records in a manner that gives an accurate and reliable account of its transactions. This constitutes unsafe …

