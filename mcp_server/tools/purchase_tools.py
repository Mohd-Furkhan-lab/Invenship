from mcp_server.mcp import tools
from analytics_engine.analysis.purchase_analysis import get_purchase_summary,get_purchases_by_supplier,get_top_purchased_products

@tools.tool
def purchase_summary():
    return get_purchase_summary()

@tools.tool
def supplier_purchase():
    return get_purchases_by_supplier()

@tools.tool()
def top_purchase_product():
    return get_top_purchased_products()
