from mcp_server.mcp import tools
from analytics_engine.analysis.purchase_analysis import get_purchase_summary,get_purchases_by_supplier,get_top_purchased_products

@tools.tool
def purchase_summary():
    """Return an overall summary of purchases (stock bought from suppliers).
    Takes no arguments. Use for general questions about purchasing activity."""
    return get_purchase_summary()

@tools.tool
def supplier_purchase():
    """Return purchase data grouped by supplier, covering all suppliers.
    Takes no arguments and cannot filter by a single supplier."""
    return get_purchases_by_supplier()

@tools.tool()
def top_purchase_product():
    """Return the most purchased products.
    Takes no arguments. Use for questions like 'which products do we buy the most'."""
    return get_top_purchased_products()