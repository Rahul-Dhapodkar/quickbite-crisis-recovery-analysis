# QuickBite Express: Data Quality Summary (Stage 1)

Scope: initial Python audit of the 8 raw CSVs. Nothing was modified. Raw files stay unchanged.

Data period: orders and reviews run from 1 Jan 2025 to 30 Sep 2025. Pre-crisis = Jan-May, crisis = Jun-Sep. There is no recovery period in the data.

## Table sizes

| Table | Rows | Grain |
|---|---|---|
| fact_orders | 149,166 | 1 row per order |
| fact_order_items | 342,994 | 1 row per order line |
| fact_ratings | 68,842 (68,825 after removing blank rows) | 1 row per rated order |
| fact_delivery_performance | 149,166 | 1 row per order |
| dim_customer | 107,776 | 1 row per customer |
| dim_restaurant | 19,995 | 1 row per restaurant |
| dim_delivery_partner_ | 15,000 | 1 row per partner |
| dim_menu_item | 342,671 | 1 row per menu item |

## Issues found

| # | Issue | Table | Size | Priority | Proposed treatment | Where |
|---|---|---|---|---|---|---|
| 1 | Fully blank rows | fact_ratings | 17 rows | High | Remove (no information in any column) | Power Query |
| 2 | Dates stored as text, 3 different formats | orders, ratings, customers | 3 columns | High | Convert with the correct format per column | Power Query |
| 3 | `delivery_partner_id` null | fact_orders | 5,635 rows (all cancelled) | Medium | Keep. Meaningful null, do not fill. | Power Query |
| 4 | Zero amounts on cancelled orders | fact_orders | 11,112 rows | High | Keep. Exclude from average order value and revenue. Lost-revenue estimates are labelled assumptions. | SQL, Power BI |
| 5 | `customer_id` missing from dim_customer | fact_orders | 5,053 orders (all cancelled) | High | Keep and label "Unknown customer". Exclude only from customer-city views. | Power Query, SQL |
| 6 | Customer city and restaurant city agree on only 15% of orders | orders, customers, restaurants | 144,113 compared | High | Restaurant city = primary. Customer city = sensitivity check. | SQL |
| 7 | Order items whose order is not in fact_orders | fact_order_items | 36,348 rows | Medium | Keep, flag, confirm in SQL integrity check | SQL |
| 8 | Same menu item twice in one order with different qty and price | fact_order_items | 33 rows | Low | Keep, investigate | SQL |
| 9 | `unit_price` (4.33-900) does not match menu `price` (25-449.99) | items, menu | whole table | Medium | Join check. Do not use for price analysis until understood. | SQL |
| 10 | Ratings are decimals (about 84% not whole numbers) | fact_ratings | 68,825 rows | Medium | State the definition used for P6 and P9 | SQL, report |
| 11 | Metadata and CSV differ (`cusini_type`, `avg_prep_time`, `employment`, `partner_type` values, Yes/No vs Y/N) | metadata vs CSVs | 5 fields | Low | Use CSV headers as the truth. Document it. | Power Query |
| 12 | `avg_prep_time_min` is text buckets, not numbers | dim_restaurant | 19,995 rows | Low | Keep as ordered categories | Power Query |
| 13 | `is_active` is a snapshot with no exit date | dim_restaurant, dim_delivery_partner_ | 1,945 inactive restaurants | Medium | Cannot date restaurant churn | Stage 6 limitation |
| 14 | No recovery-period data | all | data ends 30 Sep 2025 | High | State clearly. Do not claim to measure recovery. | Report |

Rows 5-9 came from join checks and are to be confirmed in the SQL integrity stage.

## Checked and clean

- No full-row duplicates (except the 17 blank rating rows).
- All key columns are unique: order_id, customer_id, restaurant_id, delivery_partner_id, menu_item_id, and order_id in ratings.
- Y/N flags are consistent, with no spelling variants in cities, cuisines, channels, or partner types.
- Numeric ranges are plausible: rating 1-5, sentiment -1 to +1, delivery time 25-90 mins.
- Order totals reconcile within 0.05.

## Confirmed definitions

- P3: report the literal result (no restaurant has 50 or more pre-crisis orders, maximum is 21) plus a clearly labelled lower-threshold alternative.
- Headline orders = all orders placed, with completed orders shown alongside.
- Phase comparisons use monthly averages (5 pre-crisis months vs 4 crisis months).
- Restaurant city is the primary city definition. Customer city is a sensitivity check.
- Orphan customers are kept and labelled "Unknown customer".
- No recovery is measured.

## Progress

| Stage | Status |
|---|---|
| 0 Planning | Done |
| 1 Python audit | Done |
| 2 Power Query cleaning | Next |
