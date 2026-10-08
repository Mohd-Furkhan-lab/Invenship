from mcp_server.mcp import tools
from analytics_engine.analysis.sales_analysis import get_sales_by_brand,get_sales_by_product,get_sales_by_size,get_sales_summary,get_top_revenue_products,get_top_selling_products

@tools.tool
def get_sales_by(
    brand: bool = False,
    product: bool = False,
    size: bool = False):

    data = []
    if brand:
        data.append(get_sales_by_brand())
    if product:
        data.append(get_sales_by_product())
    if size:
        data.append(get_sales_by_size())

    return data
    

@tools.tool
def sales_summary():
    return get_sales_summary()

@tools.tool
def top_revenue_product():
    return get_top_revenue_products()

@tools.tool
def top_selling_product():
    return get_top_selling_products()