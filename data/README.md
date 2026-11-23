# Data

The data is not stored in this repository. It was provided by Codebasics as a case study, and it stays the property of its owner. To rerun the project, get the files from the original source and place the eight CSV files in this folder (`data/raw/` is also ignored by Git).

## Tables

| File | Rows | One row per |
|---|---|---|
| fact_orders.csv | 149,166 | order |
| fact_order_items.csv | 342,994 | order line |
| fact_ratings.csv | 68,842 (68,825 after removing 17 blank rows) | rated order |
| fact_delivery_performance.csv | 149,166 | order |
| dim_customer.csv | 107,776 | customer |
| dim_restaurant.csv | 19,995 | restaurant |
| dim_delivery_partner_.csv | 15,000 | delivery partner |
| dim_menu_item.csv | 342,671 | menu item |

Orders and reviews run from 1 January to 30 September 2025.

## Differences between the metadata file and the CSV files

The CSV headers were used as the source of truth.

| Metadata says | CSV has |
|---|---|
| `cusini_type` | `cuisine_type` |
| `avg_prep_time` (numeric) | `avg_prep_time_min` (text ranges such as `16-25`) |
| `employment` | `employment_type` |
| `partner_type`: Third-party, In-house | Restaurant, Cloud Kitchen |
| `is_active`: Yes / No | Y / N |
| `dim_delivery_partner` | file is named `dim_delivery_partner_.csv` |

## Files derived in this project

- `powerbi/phrase_theme.csv`: our own mapping of the 27 review phrases to six complaint themes (included in the repository).
- `customer_segments.csv`: one row per customer, created by `python/build_customer_segments.py` (not included, because it holds customer-level rows).
