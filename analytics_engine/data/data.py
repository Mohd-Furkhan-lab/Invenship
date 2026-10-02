from analytics_engine.data.db import engine
import pandas as pd


def get_sales_data():
    df = pd.read_sql(
        "SELECT * FROM sales",
        engine
    )

    return df


def get_product_data():
    df = pd.read_sql(
        "SELECT * FROM products",
        engine
    )

    return df


def get_purchase_data():
    df = pd.read_sql(
        "SELECT * FROM purchase",
        engine
    )

    return df


def get_supplier_data():
    df = pd.read_sql(
        "SELECT * FROM suppliers",
        engine
    )

    return df