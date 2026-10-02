import pandas as pd

from analytics_engine.data.data import get_purchase_data, get_supplier_data

OUT_COLS = ["suid", "name", "total_quantity", "total_purchase_cost"]


def get_supplier_summary():
    suppliers = get_supplier_data()
    purchases = get_purchase_data()

    if suppliers is None or suppliers.empty:
        return []

    suppliers = suppliers.copy()

    if purchases is None or purchases.empty:
        # keep the same output shape even when there are no purchases
        suppliers["total_quantity"] = 0
        suppliers["total_purchase_cost"] = 0.0
        return suppliers[OUT_COLS].to_dict(orient="records")

    purchases = purchases.copy()
    purchases["quantity"] = pd.to_numeric(purchases["quantity"], errors="coerce").fillna(0)
    purchases["price"] = pd.to_numeric(purchases["price"], errors="coerce").fillna(0)
    purchases["cost"] = purchases["quantity"] * purchases["price"]

    purchase_summary = (
        purchases.groupby("supplier", as_index=False)
        .agg(
            total_quantity=("quantity", "sum"),
            total_purchase_cost=("cost", "sum"),
        )
    )

    result = suppliers.merge(
        purchase_summary,
        left_on="suid",
        right_on="supplier",
        how="left",
    )

    result[["total_quantity", "total_purchase_cost"]] = (
        result[["total_quantity", "total_purchase_cost"]].fillna(0)
    )
    result["total_quantity"] = result["total_quantity"].astype(int)
    result["total_purchase_cost"] = result["total_purchase_cost"].astype(float)

    return result[OUT_COLS].to_dict(orient="records")