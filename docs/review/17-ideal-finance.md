# 17. Ideal Finance Limited

`inst-ideal-finance` · notice section **L861–L967** · 6 seeded edge(s) · 21 uncited passage(s)

Read the section in `data/raw/` from L861 to L967, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1 — edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E018 — Ideal Finance Limited ← FirsTrust Savings and Loans Limited

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

### E024 — Ideal Finance Limited → FirsTrust Savings and Loans Limited

| | |
|---|---|
| relationship | `related_party_exposure_to` |
| amount | — |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L894; bog-2019-08-16-savings-loans-revocation:L861` |
| current decision | confirmed |

> Contrary to section 64 (2) of the Banks and Specialised Deposit-Taking Institutions Act, 2016 (Act 930), the institution's exposure to its related party has consistently been above the regulatory limit of 25% of net own funds (NOF). Exposures to related parties (FirstTrust Savings & Loans and Ideal Capital partners) were to the tune of Ghc63.19 million.

> 17. IDEAL FINANCE LIMITED

*Note carried from compilation:* Combined total GHS 63.19m across E024 and E025; source spells FirsTrust as FirstTrust

*Amount note:* GHS 63.19m is stated across E024 and E025 together

### E025 — Ideal Finance Limited → Ideal Capital Partners

| | |
|---|---|
| relationship | `related_party_exposure_to` |
| amount | — |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L894; bog-2019-08-16-savings-loans-revocation:L861` |
| current decision | confirmed |

> Contrary to section 64 (2) of the Banks and Specialised Deposit-Taking Institutions Act, 2016 (Act 930), the institution's exposure to its related party has consistently been above the regulatory limit of 25% of net own funds (NOF). Exposures to related parties (FirstTrust Savings & Loans and Ideal Capital partners) were to the tune of Ghc63.19 million.

> 17. IDEAL FINANCE LIMITED

*Note carried from compilation:* Combined total GHS 63.19m across E024 and E025

*Amount note:* GHS 63.19m is stated across E024 and E025 together

### E026 — Ideal Finance Limited → UNNAMED affiliates of Ideal Finance

| | |
|---|---|
| relationship | `lends_to` |
| amount | GHS 52.70m (exact) |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L924` |
| current decision | confirmed |

> Credit facilities granted to the affiliates of the Company were not approved by the Board and the exposures were not reported to Bank of Ghana in breach of Section 70(2) and 70(4) of Act 930. Total related party loans totaled GHS 52.70 million.

*Note carried from compilation:* Overlaps E024 and E025; reconcile before use

*Amount note:* total related party loans; reconcile against the GHS 63.19m figure

### I001 — Ideal Finance Limited ← Ideal Financial Holdings

| | |
|---|---|
| relationship | `owns` |
| amount | — |
| confidence | `inferred` |
| anchor | `(none — inferred)` |
| current decision | confirmed |

*Note carried from compilation:* INFERRED from name only. No source in hand states it. Excluded from headline findings until documented

### P005 — Ideal Finance Limited ← Goldstreet Fund Management Limited

| | |
|---|---|
| relationship | `placed_client_funds_with` |
| amount |  50.61 (ratio_only) |
| confidence | `documented` |
| anchor | `sec-2019-11-08-fund-manager-revocation:L835` |
| current decision | **pending** |

> 13. GOLDSTREET FUND MANAGEMENT LIMITED (FORMERLY GOLDSTREET INVESTMENTS LTD) Goldstreet Fund Management Limited (“Goldstreet”) was incorporated on the 17th December, 2014. It was licensed by the SEC as a Fund Manager on 29th September, 2015. The SEC has had a number of engagements with Goldstreet including Hearings pursuant to section 19 of Act 929, decisions have been issued by the SEC against Goldstreet with directives to take steps to comply and resolve its regulatory infractions, all to no avail. The Specific issues that led to the revocation of its licence included the following a) Failure to honour clients’ redemption requests; b) Payment of operational activities using client funds contrary to Section 160 of the Act 929; c) Non submission of statutory reports contrary to Regulations 33 (1) (a) (b) (c ) and (6) of LI 1728 d) Placement of client funds with out proper due diligence and the requisite standard of professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s Compliance Manual for Broker -Dealers, Investment Advisers and Representatives 2008. Placements include 50.61% with Ideal Finance Ltd ( in receivership) and 10.06% with First Trust Savings & Loans (in receivership)

---

## Part 2a — uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L880`**
  > The Institution's shareholders have failed to restore the bank to the required regulatory capital and liquidity levels in spite of long-standing promises that new capital was expected from foreign investors.

- **`bog-2019-08-16-savings-loans-revocation:L929`**
  > In a letter dated 25th June, 2019, the Bank of Ghana was notified about the intention to merge the operations of Ideal Finance Limited (IFL) and FirsTrust Savings and Loans Limited (FTSL). A review of the documents submitted in connection with the proposed merger and all available records obtained from the two institutions revealed that:

- **`bog-2019-08-16-savings-loans-revocation:L935`**
  > The shareholders' funds of Ideal Finance Limited (IFL) and FirsTrust Savings and Loans Limited (FTSL) as at March 2019 per the merger documents was negative GHS 62.18 million and negative GHS 93.22 million respectively.

- **`bog-2019-08-16-savings-loans-revocation:L939`**
  > The reported shareholders' funds of IFL per the last submitted prudential returns as at November 2018 was GHS 28.89 million. This was adjusted to negative GHS 117.50 million due to additional loan loss provisions and impaired investments, resulting in a decline in the reported capital adequacy ratio (CAR) of 0.52% to negative 52.18%, indicating a capital deficit of GHS 171.92 million.

- **`bog-2019-08-16-savings-loans-revocation:L945`**
  > The reported shareholders' funds of FTSL per the prudential returns for May 2019 of negative GHS 99.46 million was adjusted to negative GHS 174.10 million due to impaired investments, resulting in a further reduction in the CAR of negative 48.67% to negative 132.96%, indicating a capital deficit of GHS 189.13 million.

- **`bog-2019-08-16-savings-loans-revocation:L950`**
  > The CAR of the merged entity was therefore assessed to be negative 78.32% with a capital deficit of GHS 361.05 million. The merger will therefore, neither address the current financial challenges facing the two institutions, nor improve their future prospects. In the light of the above, BoG could not accede to the request to merge the operations of FirsTrust Savings and Loans Limited and Ideal Finance Limited.

---

## Part 2b — the rest of the section (15 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full — the extractor's vocabulary has been wrong twice already, so its judgement about what is irrelevant is not final.

- `L863` Ideal Finance Limited was incorporated in 2009 under the Companies Act, 1963 (Act 179 and licensed by the Bank of Ghana under the Non-Bank Financial I …
- `L869` Ideal Finance has been faced with severe insolvency and liquidity challenges over the past two years. The Institution faces a significant capital shor …
- `L874` The institution is also facing a severe liquidity crisis with numerous complaints received by the Financial Stability Department of the Bank of Ghana  …
- `L884` The Bank of Ghana has found key regulatory violations such as the following:
- `L887` The institution's adjusted Net worth of negative GHS 117.5 million as at end November 2018 indicates that the paid up capital is impaired in violation …
- `L891` The institution's adjusted capital adequacy ratio of negative 32.8% as at end November 2018 is in violation of Section 29(2) of Act 930.
- `L900` The institution's high non-performing loans (NPL) ratio of 23.2% was mainly attributed to poor credit risk management, thereby putting the deposits of …
- `L904` The company is yet to publish its 2018 audited accounts contrary to section 90 (2) of the Banks and Specialised Deposit-Taking Institutions Act, 2016  …
- `L910` Ideal Finance has not submitted their returns since November 2018. All efforts to get them to submit have proven futile.
- `L913` An onsite examination carried out in September 2017 revealed the following:
- `L915` The institution did not appropriately classify fifteen (15) impaired loan accounts in accordance with the requirements of the Bank of Ghana's Guide fo …
- `L920` The Institution was technically over-exposed to all its credit customers due to its negative net own funds position which is in violation of Section 6 …
- `L957` The cash reserve ratios of FTSL as at May 2019 was 0.07% compared to the regulatory minimum of 10%.
- `L960` Both institutions are unable to meet customer withdrawal needs and the Bank of Ghana has received countless complaints from customers of both institut …
- `L964` The use of landed property to shore up capital for the emerging entity is considered unacceptable in the light of the insolvent and illiquid state of  …

