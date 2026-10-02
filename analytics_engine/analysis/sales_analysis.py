import pandas as pd

from data.data import get_sales_data


def _sales_df() -> pd.DataFrame:
    df = get_sales_data()
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["total"] = pd.to_numeric(df["total"], errors="coerce").fillna(0)
    return df


def _group_sales(df: pd.DataFrame, keys, sort_by: str, limit: int | None = None):
    result = (
        df.groupby(keys, as_index=False)
        .agg(quantity_sold=("quantity", "sum"), revenue=("total", "sum"))
        .sort_values(sort_by, ascending=False)
    )
    if limit is not None:
        result = result.head(limit)
    return result.to_dict(orient="records")


def get_sales_summary():
    df = _sales_df()
    if df.empty:
        return {"total_sales": 0, "total_quantity": 0, "total_revenue": 0}

    return {
        "total_sales": int(len(df)),
        "total_quantity": int(df["quantity"].sum()),
        "total_revenue": float(df["total"].sum()),
    }


def get_top_selling_products(limit: int = 5):
    df = _sales_df()
    return [] if df.empty else _group_sales(df, ["pid", "pname"], "quantity_sold", limit)


def get_top_revenue_products(limit: int = 5):
    df = _sales_df()
    return [] if df.empty else _group_sales(df, ["pid", "pname"], "revenue", limit)


def get_sales_by_brand():
    df = _sales_df()
    return [] if df.empty else _group_sales(df, "brand", "quantity_sold")


def get_sales_by_size():
    df = _sales_df()
    return [] if df.empty else _group_sales(df, "size", "quantity_sold")


def get_sales_by_product():
    df = _sales_df()
    return [] if df.empty else _group_sales(df, ["pid", "pname"], "quantity_sold")