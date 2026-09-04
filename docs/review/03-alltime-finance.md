# 3. AllTime Finance Limited

`inst-alltime` · notice section **L239–L276** · 2 seeded edge(s) · 11 uncited passage(s)

Read the section in `data/raw/` from L239 to L276, then work through both parts below. Record every decision in `data/verification.csv`.

---

## Part 1 — edges seeded against this institution

For each: does the quote support the relationship, the direction, the amount and its basis, and the confidence class?

### E004 — AllTime Finance Limited → AllTime Capital Limited

| | |
|---|---|
| relationship | `over_exposed_to` |
| amount | GHS 18.19m (exact) |
| confidence | `documented` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L259` |
| current decision | confirmed |

> The institution is over-exposed to its related company, AllTime Capital Limited to the tune of GHS 18.19 million in violation of regulatory limits.

*Note carried from compilation:* Named counterparty with amount

### E005 — AllTime Finance Limited → UNNAMED related companies of AllTime

| | |
|---|---|
| relationship | `holds_deposits_in` |
| amount | — |
| confidence | `documented_unnamed` |
| anchor | `bog-2019-08-16-savings-loans-revocation:L273` |
| current decision | confirmed |

> and reliable account of its transactions. This is considered unsafe and unsound banking practices. Specific examples include misrepresentation of investments and deposits in related companies, and over exposure of Loan facilities to related parties.

*Note carried from compilation:* May overlap E004

---

## Part 2a — uncited passages that mention a relationship

These carry related-party, affiliate, ownership, officer or exposure wording and no edge cites them. This is where a missed relationship is most likely. For each: does it describe a relationship between this institution and another party? If so it needs an edge, and the passage needs a row in `data/evidence.csv` under the anchor shown.

- **`bog-2019-08-16-savings-loans-revocation:L266`**
  > Failure on the part of the Board to adequately exercise oversight on the institution.

---

## Part 2b — the rest of the section (10 passages)

Mostly capital adequacy, net worth and reporting breaches. Listed so the section can be scanned in full — the extractor's vocabulary has been wrong twice already, so its judgement about what is irrelevant is not final.

- `L241` AllTime Finance Limited was licensed by Bank of Ghana to operate as a finance house in July 2017 and commenced operations in August, 2017.
- `L244` A review of the institution's operations as at end-August 2018 revealed that Alltime Finance Limited was insolvent with adjusted negative capital adeq …
- `L249` The key issues that led to the revocation of license of the institution include the following:
- `L252` The institution's Net worth of negative GHS 23.15 million as at end May 2019 was in violation of Section 28(1) Act 930.
- `L256` The institution's capital adequacy ratio of negative 47.41% as at end May 2019 was in violation of Section 29(2) of Act 930.
- `L262` The Institution has not been able to meet depositors' withdrawals. The Bank of Ghana has also received many complaints from the Institution's customer …
- `L267` Failure to implement Bank of Ghana on-site examination recommendations.
- `L268` The institution amended its shareholding structure and business name without
- `L270` furnishing the details to the Bank of Ghana for approval.
- `L271` The company did not keep accounting records in a manner that gives an accurate

