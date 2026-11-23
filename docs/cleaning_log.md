# QuickBite Express: Cleaning Log (Stage 2, Excel Power Query)

Tool: Excel Power Query, workbook `cleaning.xlsx`. Raw CSVs in `raw_data/` were not modified. Each table was loaded, the automatic Changed Type step was deleted, types were set manually, and results were validated against the Stage 1 audit.

## Steps applied per table

| Table | Query name | Steps applied | Validation (against audit) |
|---|---|---|---|
| fact_ratings | fact_ratings | Removed 17 fully blank rows. Set types. `review_timestamp` converted with English (India) locale because the format is DD-MM-YYYY HH:MM. | Passed |
| fact_orders | fact_orders | Set types. `order_timestamp` is year-first, so no locale needed. | Passed |
| fact_order_items | fact_order_items | Set types only. | Passed |
| fact_delivery_performance | fact_delivery_performance | Set types only. | Passed |
| dim_customer | dim_customer | Set types. `signup_date` converted with English (India) locale (DD-MM-YYYY). | Passed |
| dim_restaurant | dim_restaurant | Set all columns to Text. | Passed |
| dim_delivery_partner_.csv | dim_delivery_partner | Set types. Query name drops the trailing underscore of the file name. | Passed |
| dim_menu_item | dim_menu_item | Set types only. | Passed |

## Deliberately not changed (decisions)

| Item | Decision | Reason |
|---|---|---|
| 5,635 null `delivery_partner_id` (all cancelled orders) | Kept as null | Meaningful null: no partner was assigned |
| 11,112 zero-amount orders (all cancelled) | Kept | Excluded from revenue and average order value in SQL |
| 5,053 orders whose `customer_id` is not in dim_customer | Not edited | Relationship checks belong to the SQL integrity stage |
| 36,348 order-item rows whose order is not in fact_orders | Kept | Confirm in SQL |
| 33 repeated menu items within an order | Kept | Not exact duplicates (different quantity and price) |
| `unit_price` vs menu `price` mismatch | Not changed | Open issue for SQL |
| Metadata vs CSV header differences | CSV headers used as the truth | `cuisine_type`, `avg_prep_time_min`, `employment_type`, partner_type values, Y/N flags |
| Inactive restaurants and partners | Kept | Needed for pre-crisis history |
| Customer city vs restaurant city mismatch | Not changed | Restaurant city is the primary city definition, decided in Stage 0 |

## Known limitations carried forward

- No recovery period: data ends on 30 Sep 2025.
- `is_active` has no exit date.
- Ratings are decimals, not whole stars.
