import pandas as pd

from data.data import get_purchase_data


def _purchase_df() -> pd.DataFrame:
    df = get_purchase_data()
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    # compute line cost once, instead of fragile lambdas inside groupby
    df["cost"] = df["quantity"] * df["price"]
    return df


def get_purchase_summary():
    df = _purchase_df()
    if df.empty:
        return {"total_purchases": 0, "total_quantity": 0, "total_cost": 0}

    return {
        "total_purchases": int(len(df)),
        "total_quantity": int(df["quantity"].sum()),
        "total_cost": float(df["cost"].sum()),
    }


def get_top_purchased_products(limit: int = 5):
    df = _purchase_df()
    if df.empty:
        return []

    result = (
        df.groupby("pid", as_index=False)
        .agg(
            quantity_purchased=("quantity", "sum"),
            purchase_cost=("cost", "sum"),
        )
        .sort_values("quantity_purchased", ascending=False)
        .head(limit)
    )
    return result.to_dict(orient="records")


def get_purchases_by_supplier():
    df = _purchase_df()
    if df.empty:
        return []

    result = (
        df.groupby("supplier", as_index=False)
        .agg(
            quantity_purchased=("quantity", "sum"),
            purchase_cost=("cost", "sum"),
        )
        .sort_values("quantity_purchased", ascending=False)
    )
    return result.to_dict(orient="records")