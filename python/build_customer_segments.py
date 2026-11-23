"""
Builds customer_segments.csv for Power BI page 2 (Customer Retention and Recovery).

Rules (same as the SQL stage):
- Base: customers with at least one completed order from Jan to May 2025.
- Stopped: no completed order from Jun to Sep 2025.
- High-value: top 5% by Jan-May spend (percent rank >= 0.95).
- Segment (first rule that applies): 1 High-value, 2 Repeat (2+ orders),
  3 Single-order rated 4.5+ before June, 4 Single-order, other.

Usage: python build_customer_segments.py <folder with the CSV files> <output file>
The folder must contain fact_orders.csv, fact_ratings.csv and dim_customer.csv.
"""
import sys
import pandas as pd

data_dir = sys.argv[1] if len(sys.argv) > 1 else "."
out_file = sys.argv[2] if len(sys.argv) > 2 else "customer_segments.csv"

orders = pd.read_csv(f"{data_dir}/fact_orders.csv")
ratings = pd.read_csv(f"{data_dir}/fact_ratings.csv").dropna(subset=["order_id"])
customers = pd.read_csv(f"{data_dir}/dim_customer.csv").set_index("customer_id")

orders["ts"] = pd.to_datetime(orders["order_timestamp"])
ratings["ts"] = pd.to_datetime(ratings["review_timestamp"], format="%d-%m-%Y %H:%M")

completed = orders[orders["is_cancelled"] == "N"]
pre = completed[completed["ts"] < "2025-06-01"]
crisis = completed[completed["ts"] >= "2025-06-01"]

# one row per customer: earlier orders and spend
seg = pre.groupby("customer_id").agg(pre_orders=("order_id", "size"),
                                     pre_spend=("total_amount", "sum"))

# percent rank of spend, same as PERCENT_RANK() in SQL
seg["pct_rank"] = (seg["pre_spend"].rank(method="min") - 1) / (len(seg) - 1)

# crisis activity and earlier rating
seg["crisis_orders"] = crisis.groupby("customer_id").size().reindex(seg.index).fillna(0).astype(int)
seg["status"] = seg["crisis_orders"].apply(lambda n: "Still ordering" if n > 0 else "Stopped")
seg["is_high_value"] = seg["pct_rank"].apply(lambda x: "Y" if x >= 0.95 else "N")
seg["pre_avg_rating"] = ratings[ratings["ts"] < "2025-06-01"].groupby("customer_id")["rating"].mean().reindex(seg.index)


def pick_segment(row):
    if row["pct_rank"] >= 0.95:
        return "1 High-value"
    if row["pre_orders"] >= 2:
        return "2 Repeat"
    if pd.notna(row["pre_avg_rating"]) and row["pre_avg_rating"] >= 4.5:
        return "3 Single-order, rated 4.5+"
    return "4 Single-order, other"


seg["segment"] = seg.apply(pick_segment, axis=1)
seg["pre_order_band"] = seg["pre_orders"].apply(lambda n: "4+" if n >= 4 else str(n))
seg["customer_city"] = customers["city"].reindex(seg.index)
seg["acquisition_channel"] = customers["acquisition_channel"].reindex(seg.index)

seg["pre_spend"] = seg["pre_spend"].round(2)
seg["pre_avg_rating"] = seg["pre_avg_rating"].round(2)

columns = ["customer_id", "pre_orders", "pre_spend", "crisis_orders", "status", "is_high_value",
           "pre_avg_rating", "segment", "pre_order_band", "customer_city", "acquisition_channel"]
seg.reset_index()[columns].to_csv(out_file, index=False)

print("rows:", len(seg))
print(seg.groupby("segment")["status"].agg(customers="size", stopped=lambda s: (s == "Stopped").sum()))
