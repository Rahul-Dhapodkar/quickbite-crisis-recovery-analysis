import os
import pandas as pd
from sqlalchemy import create_engine

# Set these before running. Do not write your password inside this file.
#   Windows (cmd):  set MYSQL_USER=your_user   and   set MYSQL_PASSWORD=your_password
folder = r"path\to\cleaned_csv_files"          # folder with your _clean.csv files
database = "quickbite"                          # name of the MySQL database
user = os.environ["MYSQL_USER"]
password = os.environ["MYSQL_PASSWORD"]
engine = create_engine(f"mysql+pymysql://{user}:{password}@localhost:3306/{database}")

# table name in MySQL : cleaned file
# The tables must already exist, because the rows are appended to them.
files = {
    "fact_orders":               "fact_orders_clean.csv",
    "dim_restaurant":            "dim_restaurant_clean.csv",
    "dim_delivery_partner":      "dim_delivery_partner_clean.csv",
    "dim_menu_item":             "dim_menu_item_clean.csv",
    "fact_delivery_performance": "fact_delivery_performance_clean.csv",
    "fact_ratings":              "fact_ratings_clean.csv",
    "fact_order_items":          "fact_order_items_clean.csv",
}

for table, file in files.items():
    path = folder + "\\" + file
    # utf-8-sig removes the hidden marker Excel adds at the start of a CSV file
    # keep_default_na=False and na_values=[""] make only truly empty cells become NULL
    df = pd.read_csv(path, encoding="utf-8-sig", keep_default_na=False, na_values=[""])
    if df.columns[0] == "Column1":      # extra header line present
        df = pd.read_csv(path, encoding="utf-8-sig", header=1,
                         keep_default_na=False, na_values=[""])
        print(table, "had an extra header line, skipped it")
    print(table, "rows read:", len(df))
    df.to_sql(table, engine, if_exists="append", index=False, chunksize=10000)
    print(table, "loaded")
