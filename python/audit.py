import pandas as pd

folder = r"path\to\csv\files"   # change this to the folder with the original CSV files

files = {
    "orders":    "fact_orders.csv",
    "items":     "fact_order_items.csv",
    "ratings":   "fact_ratings.csv",
    "delivery":  "fact_delivery_performance.csv",
    "customers": "dim_customer.csv",
    "restaurants": "dim_restaurant.csv",
    "partners":  "dim_delivery_partner_.csv",   # note the trailing underscore
    "menu":      "dim_menu_item.csv",
}

data = {name: pd.read_csv(folder + "\\" + f) for name, f in files.items()}

#for name, df in data.items():
#    print(name, df.shape)

for name, df in data.items():
    print("\n====", name)
    print("duplicate rows:", df.duplicated().sum())
    nulls = df.isna().sum()
    print("nulls:", nulls[nulls > 0].to_dict())
    print(df.dtypes.to_string())

# --- dates ---
o = data["orders"]
r = data["ratings"]
c = data["customers"]

o_dt = pd.to_datetime(o["order_timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
r_dt = pd.to_datetime(r["review_timestamp"], format="%d-%m-%Y %H:%M", errors="coerce")
c_dt = pd.to_datetime(c["signup_date"], format="%d-%m-%Y", errors="coerce")

print("orders  :", o_dt.isna().sum(), "unparseable |", o_dt.min(), "to", o_dt.max())
print("reviews :", r_dt.isna().sum(), "unparseable |", r_dt.min(), "to", r_dt.max())
print("signups :", c_dt.isna().sum(), "unparseable |", c_dt.min(), "to", c_dt.max())

# --- categorical values ---
print(o["is_cod"].value_counts(dropna=False).to_dict())
print(o["is_cancelled"].value_counts(dropna=False).to_dict())
print(data["restaurants"]["partner_type"].value_counts(dropna=False).to_dict())
print(data["restaurants"]["is_active"].value_counts(dropna=False).to_dict())
print(data["restaurants"]["cuisine_type"].value_counts(dropna=False).to_dict())
print(data["customers"]["city"].value_counts(dropna=False).to_dict())
print(data["customers"]["acquisition_channel"].value_counts(dropna=False).to_dict())


print(data["orders"][["subtotal_amount", "discount_amount", "delivery_fee", "total_amount"]].describe().round(2))
print(data["items"][["quantity", "unit_price", "item_discount", "line_total"]].describe().round(2))
print(data["delivery"][["actual_delivery_time_mins", "expected_delivery_time_mins", "distance_km"]].describe().round(2))
print(data["ratings"][["rating", "sentiment_score"]].describe().round(2))
print(data["menu"][["price"]].describe().round(2))
print(data["partners"][["avg_rating"]].describe().round(2))

# -- Duplicate Key --
o = data["orders"]
print(pd.crosstab(o["is_cancelled"], o["subtotal_amount"] == 0))

print("orders      order_id dup:", data["orders"]["order_id"].duplicated().sum())
print("delivery    order_id dup:", data["delivery"]["order_id"].duplicated().sum())
print("customers   customer_id dup:", data["customers"]["customer_id"].duplicated().sum())
print("restaurants restaurant_id dup:", data["restaurants"]["restaurant_id"].duplicated().sum())
print("partners    partner_id dup:", data["partners"]["delivery_partner_id"].duplicated().sum())
print("menu        menu_item_id dup:", data["menu"]["menu_item_id"].duplicated().sum())

rt = data["ratings"].dropna(subset=["order_id"])      # ignore the 17 blank rows
print("ratings     order_id dup:", rt["order_id"].duplicated().sum())

it = data["items"]
print("items       same order + menu item repeated:", it.duplicated(["order_id", "menu_item_id"]).sum())

