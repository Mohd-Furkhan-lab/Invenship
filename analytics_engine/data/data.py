from .db import engine
import pandas as pd

# sales_data = pd.read_sql(
#     "SELECT * from sales",
#     engine
# )

purchase_data = pd.read_sql(
    "SELECT * from purchase",
    engine
)

product_data = pd.read_sql(
    "SELECT * from products",
    engine
)

with open("products.csv", "w") as file:

    file.write(",".join(product_data.columns) + "\n")

    for row in product_data.itertuples(index=False):
        file.write(",".join(map(str, row)) + "\n")