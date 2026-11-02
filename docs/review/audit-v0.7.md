# Check sheet: the v0.7 pre-release audit

14 edges changed or added in the audit, each set back to `pending` and then re-checked by hand. For each, open the notice at the line given (`data/raw/` holds the working text; `sources/` the PDF) and decide whether the edge now says what the passage says: the relationship, the direction, the confidence class, and any amount or date.

Record each decision in `data/verification.csv`: `confirmed` if it is right as it stands, `corrected` with a note if you change it, `rejected` if the edge should not exist.

Why each change was made is in `data/changelog.csv`, C029 to C036.

---

## E002: Adom Savings and Loans Limited → UNNAMED related parties of Adom

| field | before the audit | now |
|---|---|---|
| relationship | `lends_to` | `over_exposed_to` |

*Why:* Changed in the v0.7 pre-release audit: relationship lends_to -> over_exposed_to: the passage states a breach of the statutory limit and does not say the exposure is lending. Previously confirmed on 2026-09-04 by Samuel Ato Kwame Baah. Awaiting a re-check against the source.

`L224` (BOG)

> Non-performing related party exposures were far in excess of the statutory limits.

*Note on the edge:* Exposures stated to be far in excess of the statutory limits; no amount stated. Shares Adom's placeholder with E003, although the notice does not say the fee recipients and these counterparties are the same parties

Decision: **confirmed**, 14 September 2026, Samuel Ato Kwame Baah

---

## E013: UNNAMED major shareholder of First Allied → First Allied Savings and Loans Limited

| field | before the audit | now |
|---|---|---|
| source_entity_id | `inst-first-allied` | `ph-first-allied-shareholder` |
| target_entity_id | `ph-first-allied-shareholder` | `inst-first-allied` |
| relationship | `controls` | `owns` |
| evidence_anchors | bog-2019-08-16-savings-loans-revocation:L580 | bog-2019-08-16-savings-loans-revocation:L543 |

*Why:* Changed in the v0.7 pre-release audit: direction reversed and relationship controls -> owns: the edge said First Allied controls its own majority shareholder; L543 names the Board Chairman/Majority Shareholder of the institution. Anchor moved from L580, which does not state the relationship, to L543. Previously confirmed on 2026-09-04 by Samuel Ato Kwame Baah. Awaiting a re-check against the source.

`L543` (BOG)

> First Allied Savings & Loans Ltd. (FASL) was found to be insolvent with a negative Capital Adequacy Ratio and a negative net worth as of 31 March 2018. The Bank of Ghana directed the Board Chairman/Majority Shareholder and Management of the Institution

*Note on the edge:* Stated as the institution's Board Chairman/Majority Shareholder (L543); identity and shareholding not stated

Decision: **confirmed**, 14 September 2026, Samuel Ato Kwame Baah

---

## E016: First African Savings and Loans Limited → UNNAMED related parties of First African

| field | before the audit | now |
|---|---|---|
| relationship | `lends_to` | `related_party_exposure_to` |

*Why:* Changed in the v0.7 pre-release audit: relationship lends_to -> related_party_exposure_to: the passage does not say the exposure is lending. Previously confirmed on 2026-09-04 by Samuel Ato Kwame Baah. Awaiting a re-check against the source.

`L630` (BOG)

> The institution is unable to meet the withdrawal demands of its depositors. The institution has related party exposure which it is unable to recover.

*Note on the edge:* Related party exposure the institution is unable to recover; its form is not stated. May overlap E015

Decision: **confirmed**, 14 September 2026, Samuel Ato Kwame Baah

---

## E018: FirsTrust Savings and Loans Limited → Ideal Finance Limited

| field | before the audit | now |
|---|---|---|
| amount_note | projected cash injection for the proposed merger, not an exposure | Projected cash injection of GHS 127.00m into the merged entity, if approved; not a flow between the two parties |
| evidence_anchors | bog-2019-08-16-savings-loans-revocation:L702 | bog-2019-08-16-savings-loans-revocation:L702; bog-2019-08-16-savings-loans-revocation:L929 |

*Why:* Changed in the v0.7 pre-release audit: anchor L929 added for the 25 June 2019 letter; notes separate the letter's date from the request's. Previously confirmed on 2026-09-04 by Samuel Ato Kwame Baah. Awaiting a re-check against the source.

`L702` (BOG)

> Bank of Gnana declined a request dated 25th July, 2019 to merge the operations of FirsTrust Savings and Loans Limited and Ideal Finance Limited because the two institutions under consideration are both insolvent and illiquid. The total projected cash injection of GHS 127.00 million, if approved, will lead to total shareholders' funds of the proposed merged entity from negative GHS 291.60 million to negative GHS 164.60 million and CAR from negative 78.32% to negative 47.26% leaving a significant capital deficit of GHS 234.05 million. The merger was therefore, not going to address the current financial challenges facing the two institutions, or improve their future prospects.

`L929` (BOG)

> In a letter dated 25th June, 2019, the Bank of Ghana was notified about the intention to merge the operations of Ideal Finance Limited (IFL) and FirsTrust Savings and Loans Limited (FTSL).

*Note on the edge:* Notification letter dated 25 June 2019 (L929); the refusal cites a request dated 25 July 2019 (L702). Refused, both being insolvent

Decision: **confirmed**, 14 September 2026, Samuel Ato Kwame Baah

---

## E019: Global Access Savings and Loans Company Limited → UNNAMED majority shareholder of Global Access

| field | before the audit | now |
|---|---|---|
| confidence | `documented` | `documented_unnamed` |

*Why:* Changed in the v0.7 pre-release audit: confidence documented -> documented_unnamed: the counterparty is the unnamed majority shareholder. Previously confirmed on 2026-09-04 by Samuel Ato Kwame Baah. Awaiting a re-check against the source.

`L737` (BOG)

> The institution assumed the liability of a loan contracted by the majority shareholder amounting GHS 2.91 million. The loan amount was injected into the institution as equity capital. The liability was however concealed as a suspense account in the books of Global Access Savings and Loans Limited.

*Note on the edge:* Loan contracted by the majority shareholder, concealed in a suspense account; the shareholder is not named

Decision: **confirmed**, 14 September 2026, Samuel Ato Kwame Baah

---

## E020: Global Access Savings and Loans Company Limited → UNNAMED majority shareholder of Global Access

| field | before the audit | now |
|---|---|---|
| confidence | `documented` | `documented_unnamed` |
| evidence_anchors | bog-2019-08-16-savings-loans-revocation:L741; bog-2019-08-16-savings-loans-revocation:L713 | bog-2019-08-16-savings-loans-revocation:L741 |

*Why:* Changed in the v0.7 pre-release audit: confidence documented -> documented_unnamed; section-heading anchor L713, added only to satisfy rule 12 for a named counterparty, removed. Previously confirmed on 2026-09-04 by Samuel Ato Kwame Baah. Awaiting a re-check against the source.

`L741` (BOG)

> The institution continues to record accumulated losses due mainly to high rent expenses paid to the majority shareholder for the use of its premises.

*Note on the edge:* Rent paid to the majority shareholder for the use of its premises; no amount stated

Decision: **confirmed**, 14 September 2026, Samuel Ato Kwame Baah

---

## E026: Ideal Finance Limited → UNNAMED affiliates of Ideal Finance

| field | before the audit | now |
|---|---|---|
| amount_note | total related party loans; reconcile against the GHS 63.19m figure | Total related party loans per the onsite examination of September 2017 (L913); the GHS 63.19m on E024 and E025 is a later figure |
| as_at_date | none | 2017-09 |

*Why:* Changed in the v0.7 pre-release audit: as_at_date 2017-09 added: the figure comes from the September 2017 onsite examination, which explains why it differs from the GHS 63.19m. Previously confirmed on 2026-09-04 by Samuel Ato Kwame Baah. Awaiting a re-check against the source.

`L924` (BOG)

> Credit facilities granted to the affiliates of the Company were not approved by the Board and the exposures were not reported to Bank of Ghana in breach of Section 70(2) and 70(4) of Act 930. Total related party loans totaled GHS 52.70 million.

*Note on the edge:* Overlaps E024 and E025; reconcile before use

Decision: **confirmed**, 14 September 2026, Samuel Ato Kwame Baah

---

## E032: uniCredit Ghana Limited → uniSecurities Limited

| field | before the audit | now |
|---|---|---|
| evidence_anchors | bog-2019-08-16-savings-loans-revocation:L1127; bog-2019-08-16-savings-loans-revocation:L1100 | bog-2019-08-16-savings-loans-revocation:L1127; bog-2019-08-16-savings-loans-revocation:L1100; bog-2019-08-16-savings-loans-revocation:L1108 |

*Why:* Changed in the v0.7 pre-release audit: anchor L1108 added: it is the passage that states the over-exposure to uniSecurities, a sister company. Previously confirmed on 2026-09-04 by Samuel Ato Kwame Baah. Awaiting a re-check against the source.

`L1127` (BOG)

> The institution's adjusted capital adequacy ratio of negative 97.83% as at end May 2019 is in violation of Section 29(2) of Act 930. This is mainly due to the non- performing related party exposures of GHS 160.10 million to uniSecurities which is far in excess of its negative networth.

`L1100` (BOG)

> 22. UNICREDIT GHANA LIMITED

`L1108` (BOG)

> The Institution is currently over exposed to a related party, uniSecurities Limited, a sister company.

*Note on the edge:* Largest single named-counterparty exposure in the notice

Decision: **confirmed**, 14 September 2026, Samuel Ato Kwame Baah

---

## E045: CDH Savings and Loans Ltd. → UNNAMED related companies of CDH

| field | before the audit | now |
|---|---|---|
| source_entity_id | none | `inst-cdh` |
| target_entity_id | none | `ph-cdh-related-companies` |
| relationship | *(new edge)* | `placed_funds_with` |
| amount_value | none | none |
| amount_currency | none | none |
| amount_unit | none | none |
| amount_basis | none | none |
| amount_note | none | none |
| as_at_date | none | none |
| confidence | none | `documented_unnamed` |
| evidence_anchors | none | bog-2019-08-16-savings-loans-revocation:L381 |

*Why:* Changed in the v0.7 pre-release audit: added in the pre-release audit. Awaiting a re-check against the source.

`L381` (BOG)

> The inability of CDH to access placements/investments with other insolvent financial institutions, including related companies, worsened its solvency liquidity situation.

*Note on the edge:* Placements/investments with related companies that CDH could not access; count and amount not stated. Held apart from ph-cdh-affiliates, because the notice says 'related companies' here and 'affiliate companies' elsewhere and does not say they are the same

Decision: **confirmed**, 14 September 2026, Samuel Ato Kwame Baah

---

## E046: GN Savings and Loans Ltd. → UNNAMED related parties of GN in the Groupe Nduom network

| field | before the audit | now |
|---|---|---|
| source_entity_id | none | `inst-gn` |
| target_entity_id | none | `ph-gn-related-parties` |
| relationship | *(new edge)* | `over_exposed_to` |
| amount_value | none | none |
| amount_currency | none | none |
| amount_unit | none | none |
| amount_basis | none | none |
| amount_note | none | none |
| as_at_date | none | none |
| confidence | none | `documented_unnamed` |
| evidence_anchors | none | bog-2019-08-16-savings-loans-revocation:L826 |

*Why:* Changed in the v0.7 pre-release audit: added in the pre-release audit. Awaiting a re-check against the source.

`L826` (BOG)

> Contrary to section 64 (2) of the Banks and Specialised Deposit-Taking Institutions Act, 2016 (Act 930), the institution's exposure to its related party has consistently been above the regulatory limit of 25% of net own funds (NOF). Exposures to other affiliates companies were mainly payments made by the bank on behalf of such affiliates.

*Note on the edge:* Exposure to its related party consistently above the 25% limit of net own funds; other affiliate exposures were mainly payments made on their behalf. The same wording produced E024 and E025 for Ideal Finance

Decision: **confirmed**, 14 September 2026, Samuel Ato Kwame Baah

---

## E047: UNNAMED parent company of Crest → Crest Finance House Limited

| field | before the audit | now |
|---|---|---|
| source_entity_id | none | `ph-crest-parent` |
| target_entity_id | none | `inst-crest` |
| relationship | *(new edge)* | `owns` |
| amount_value | none | none |
| amount_currency | none | none |
| amount_unit | none | none |
| amount_basis | none | none |
| amount_note | none | none |
| as_at_date | none | none |
| confidence | none | `documented_unnamed` |
| evidence_anchors | none | bog-2019-08-16-savings-loans-revocation:L434 |

*Why:* Changed in the v0.7 pre-release audit: added in the pre-release audit. Awaiting a re-check against the source.

`L434` (BOG)

> Non-performing exposures to its parent company and a company in which the Chief Executive Officer is a director in excess of statutory limit. The exposures also contributed significantly to the institution's liquidity challenges.

*Note on the edge:* 'its parent company'; identity and shareholding not stated

Decision: **confirmed**, 14 September 2026, Samuel Ato Kwame Baah

---

## E048: Dream Finance Limited → UNNAMED six related companies of Dream

| field | before the audit | now |
|---|---|---|
| source_entity_id | none | `inst-dream` |
| target_entity_id | none | `ph-dream-6` |
| relationship | *(new edge)* | `funded_projects_of` |
| amount_value | none | none |
| amount_currency | none | none |
| amount_unit | none | none |
| amount_basis | none | none |
| amount_note | none | none |
| as_at_date | none | none |
| confidence | none | `documented_unnamed` |
| evidence_anchors | none | bog-2019-08-16-savings-loans-revocation:L472 |

*Why:* Changed in the v0.7 pre-release audit: added in the pre-release audit. Awaiting a re-check against the source.

`L472` (BOG)

> The use of depositors' funds to finance related party projects. The institution is over exposed to six (6) of its related companies. The non-performing related party exposures, has contributed significantly to the liquidity challenges of the institution.

*Note on the edge:* 'The use of depositors' funds to finance related party projects', the wording that produced E031 for ASN. The notice does not say the projects belong to the six related companies of E011; attached to Dream's related-party placeholder, as E002 and E003 share Adom's

Decision: **confirmed**, 14 September 2026, Samuel Ato Kwame Baah

---

## E049: FirsTrust Savings and Loans Limited → UNNAMED six related companies of FirsTrust

| field | before the audit | now |
|---|---|---|
| source_entity_id | none | `inst-firstrust` |
| target_entity_id | none | `ph-firstrust-6` |
| relationship | *(new edge)* | `funded_projects_of` |
| amount_value | none | none |
| amount_currency | none | none |
| amount_unit | none | none |
| amount_basis | none | none |
| amount_note | none | none |
| as_at_date | none | none |
| confidence | none | `documented_unnamed` |
| evidence_anchors | none | bog-2019-08-16-savings-loans-revocation:L685 |

*Why:* Changed in the v0.7 pre-release audit: added in the pre-release audit. Awaiting a re-check against the source.

`L685` (BOG)

> The use of depositors' funds to finance related party projects. The institution is over exposed to six (6) of its related companies to the tune of GHS 17.93 million. The non-performing related party exposures, has contributed significantly to the liquidity challenges of the institution.

*Note on the edge:* 'The use of depositors' funds to finance related party projects', the wording that produced E031 for ASN. The notice does not say the projects belong to the six related companies of E017; attached to FirsTrust's related-party placeholder, as E002 and E003 share Adom's

Decision: **confirmed**, 14 September 2026, Samuel Ato Kwame Baah

---

## S014: Gold Coast Fund Management Limited → Ghana Growth Fund

| field | before the audit | now |
|---|---|---|
| amount_note | 99.41% of funds under management; a ratio, not an amount | 99.41% of funds under management per the 2nd Quarter 2018 placement report; a ratio, not an amount |
| as_at_date | none | 2018-06-30 |

*Why:* Changed in the v0.7 pre-release audit: as_at_date 2018-06-30 added from the 2nd Quarter 2018 placement report. Previously confirmed on 2026-09-04 by Samuel Ato Kwame Baah. Awaiting a re-check against the source.

`L658` (SEC)

> 4. BLACKSHIELD CAPITAL MANAGEMENT LTD (FORMERLY GOLD COAST FUND MANAGEMENT LIMITED) Blackshield Capital Management Ltd (formerly Gold Coa st Fund Management Limited), “Blackshield”, was incorporated on the 12th August, 1993 prior to the passage of the Act and was licensed by the Commission on 12th August, 2013. On 11th July, 2019, the firm changed its name to Blackshield Capital Management Ltd. The SEC has had a number of engagements with Blackshield including Hearings pursuant to section 19 of Act 929, decisions have been issued by the SEC against Blackshield with directives to take steps to comply and resolve its regulatory infractions, all to no avail. The Specific issues that led to the revocation of its licence included the following: a) Failure to honour clients’ redemption requests b) Placement of client funds with related parties without proper due diligence and the requisite standard of professional conduct contrary to Paragraphs, 2, 3, 6 and 13 of Part X of the Commission’s Compliance Manual for Broker -Dealers, Investment Advisers an d Representatives 2008. According to Blackshield’s 2nd Quarter 2018 Placement Report, 99.41% of Blackshield’s funds under management had been placed with an unregulated related entity, Ghana Growth Fund Limited (now Gold Coast Advisors Limited).

*Note on the edge:* The Bank of Ghana names both as sister companies of GN and calls them SEC-licensed; the Commission calls Ghana Growth Fund an unregulated related entity

Decision: **confirmed**, 14 September 2026, Samuel Ato Kwame Baah

---
