from mcp_server.mcp import tools
from analytics_engine.analysis.product_analysis import get_low_stock_products,get_inventory_summary,get_most_expensive_products,get_out_of_stock_products,get_products_by_brand

@tools.tool
def inventory_summary():
    return get_inventory_summary()

@tools.tool
def low_stock():
    return get_low_stock_products

@tools.tool
def out_of_stock():
    return get_out_of_stock_products()

@tools.tool
def most_expensive_product():
    return get_most_expensive_products()

@tools.tool
def product_by_brand():
    return get_products_by_brand()
