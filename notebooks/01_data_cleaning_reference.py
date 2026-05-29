"""
Online Retail II - cleaning & RFM reference pipeline
----------------------------------------------------
Validated reference version. Fixes two issues found in the first pass:
  (1) exact duplicate rows were not removed (~26k rows, ~GBP 369k inflation)
  (2) unidentified customers were dropped from ALL revenue, understating
      commercial revenue by ~15% (GBP 3.1M).

Approach: two clean layers feeding one lean dashboard.
  - sales_all       -> identified + unidentified, for COMMERCIAL KPIs
                       (revenue, country, product). True total revenue.
  - sales_identified-> only rows with a Customer ID, basis for RFM /
                       segmentation / cohort (customer-level analysis).

Run from the notebooks/ folder:  python 01_data_cleaning_reference.py
"""

import pandas as pd

RAW = "../data/raw/online_retail_II.csv"
OUT = "../data/processed/"


def segment_customer(row):
    """Same segmentation logic as the original notebook (kept intentionally)."""
    r, f, m = int(row["R_Score"]), int(row["F_Score"]), int(row["M_Score"])
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif r >= 3 and f >= 3 and m >= 3:
        return "Loyal Customers"
    elif r >= 4 and f <= 2:
        return "Potential Loyalists"
    elif r <= 2 and m >= 4:
        return "At Risk"
    else:
        return "Others"


# ---- load ----------------------------------------------------------------
df = pd.read_csv(RAW, dtype={"Invoice": str, "StockCode": str})
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# ---- (1) drop exact duplicates -------------------------------------------
before = len(df)
df = df.drop_duplicates()
print(f"Dropped {before - len(df):,} exact-duplicate rows")

# revenue
df["Revenue"] = df["Quantity"] * df["Price"]

# ---- split returns / cancellations ---------------------------------------
is_return = df["Invoice"].str.startswith("C", na=False) | (df["Quantity"] < 0)
returns_df = df[is_return].copy()

# ---- sales layers --------------------------------------------------------
# layer A: ALL valid sales (incl. unidentified customers) -> commercial KPIs
sales_all = df[(~is_return) & (df["Price"] > 0)].copy()
sales_all["YearMonth"] = sales_all["InvoiceDate"].dt.to_period("M").astype(str)
sales_all["Country"] = sales_all["Country"].replace("EIRE", "Ireland")

# layer B: identified customers only -> RFM / segmentation / cohort
sales_identified = sales_all.dropna(subset=["Customer ID"]).copy()
sales_identified["Customer ID"] = sales_identified["Customer ID"].astype("int64")

print(f"Returns/cancellations : {len(returns_df):,}")
print(f"Sales (all)           : {len(sales_all):,}  | revenue GBP {sales_all['Revenue'].sum():,.0f}")
print(f"Sales (identified)    : {len(sales_identified):,}  | revenue GBP {sales_identified['Revenue'].sum():,.0f}")

# ---- RFM on identified customers -----------------------------------------
snapshot = sales_identified["InvoiceDate"].max()
cm = (
    sales_identified.groupby("Customer ID")
    .agg(TotalOrders=("Invoice", "nunique"),
         TotalRevenue=("Revenue", "sum"),
         LastPurchaseDate=("InvoiceDate", "max"))
    .reset_index()
    .rename(columns={"Customer ID": "CustomerID"})
)
cm["Recency"] = (snapshot - cm["LastPurchaseDate"]).dt.days
cm["R_Score"] = pd.qcut(cm["Recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
cm["F_Score"] = pd.qcut(cm["TotalOrders"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
cm["M_Score"] = pd.qcut(cm["TotalRevenue"], 5, labels=[1, 2, 3, 4, 5]).astype(int)
cm["RFM_Score"] = cm[["R_Score", "F_Score", "M_Score"]].astype(str).agg("".join, axis=1)
cm["Segment"] = cm.apply(segment_customer, axis=1)

# ---- segment summary (with % shares for the treemap story) ---------------
seg = (
    cm.groupby("Segment")
    .agg(CustomerCount=("CustomerID", "count"),
         TotalRevenue=("TotalRevenue", "sum"),
         AvgOrders=("TotalOrders", "mean"))
    .reset_index()
)
seg["RevenuePct"] = (seg["TotalRevenue"] / seg["TotalRevenue"].sum() * 100).round(1)
seg["CustomerPct"] = (seg["CustomerCount"] / seg["CustomerCount"].sum() * 100).round(1)
seg["TotalRevenue"] = seg["TotalRevenue"].round(2)
seg["AvgOrders"] = seg["AvgOrders"].round(2)
seg = seg.sort_values("TotalRevenue", ascending=False)

# ---- exports -------------------------------------------------------------
sales_all.to_csv(OUT + "clean_sales_all.csv", index=False)
sales_identified.to_csv(OUT + "clean_sales_identified.csv", index=False)
returns_df.to_csv(OUT + "returns.csv", index=False)
cm.to_csv(OUT + "customer_metrics.csv", index=False)
seg.to_csv(OUT + "segment_summary.csv", index=False)
print("\nExported 5 files to data/processed/")
print(seg.to_string(index=False))
