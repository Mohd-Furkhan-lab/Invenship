from mcp_server.app import tools
from analytics_engine.analysis.product_analysis import get_low_stock_products,get_inventory_summary,get_most_expensive_products,get_out_of_stock_products,get_products_by_brand

@tools.tool
def inventory_summary():
    """Return an overall summary of the current inventory.
    Takes no arguments. Use for general questions about stock levels and inventory status."""
    return get_inventory_summary()

@tools.tool
def low_stock():
    """Return the products that are running low on stock.
    Takes no arguments. Use for questions like 'which products need restocking soon'."""
    return get_low_stock_products()

@tools.tool
def out_of_stock():
    """Return the products that are completely out of stock.
    Takes no arguments. Use for questions like 'which products are unavailable'."""
    return get_out_of_stock_products()

@tools.tool
def most_expensive_product():
    """Return the most expensive products in the catalog.
    Takes no arguments. Use for questions about the highest-priced products."""
    return get_most_expensive_products()

@tools.tool
def product_by_brand():
    """Return product data organized by brand, covering all brands.
    Takes no arguments and cannot filter by a single brand."""
    return get_products_by_brand()