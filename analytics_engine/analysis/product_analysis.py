import pandas as pd

from analytics_engine.data.data import get_product_data

PRODUCT_COLS = ["pid", "pname", "brand", "size", "price", "stock"]


def _product_df() -> pd.DataFrame:
    # get_product_data() already returns a DataFrame
    df = get_product_data()
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    # SQL NUMERIC columns arrive as Decimal; coerce so math and JSON work
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["stock"] = pd.to_numeric(df["stock"], errors="coerce").fillna(0)
    return df


def get_inventory_summary():
    df = _product_df()
    if df.empty:
        return {"total_products": 0, "total_stock": 0, "inventory_value": 0}

    return {
        "total_products": int(len(df)),
        "total_stock": int(df["stock"].sum()),
        "inventory_value": float((df["price"] * df["stock"]).sum()),
    }


def get_low_stock_products(threshold: int = 10):
    df = _product_df()
    if df.empty:
        return []

    result = df[df["stock"] <= threshold][PRODUCT_COLS].sort_values("stock")
    return result.to_dict(orient="records")


def get_out_of_stock_products():
    df = _product_df()
    if df.empty:
        return []

    return df[df["stock"] <= 0][PRODUCT_COLS].to_dict(orient="records")


def get_products_by_brand():
    df = _product_df()
    if df.empty:
        return []

    df = df.assign(inventory_value=df["price"] * df["stock"])
    result = (
        df.groupby("brand", as_index=False)
        .agg(
            product_count=("pid", "count"),
            total_stock=("stock", "sum"),
            inventory_value=("inventory_value", "sum"),
        )
        .sort_values("inventory_value", ascending=False)
    )
    return result.to_dict(orient="records")


def get_most_expensive_products(limit: int = 5):
    df = _product_df()
    if df.empty:
        return []

    result = (
        df[PRODUCT_COLS]
        .sort_values("price", ascending=False)
        .head(limit)
    )
    return result.to_dict(orient="records")