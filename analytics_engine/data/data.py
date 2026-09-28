from .db import engine
import pandas as pd

salse_data = pd.read_sql(
    engine,
    "SELECT * from sales"
)

purchase_data = pd.read_sql(
    engine,
    "SELECT * from purchases"
)

product_data = pd.read_sql(
    engine,
    "SELECT * from products"
)