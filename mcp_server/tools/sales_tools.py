from mcp_server.app import tools
from analytics_engine.analysis.sales_analysis import get_sales_by_brand,get_sales_by_product,get_sales_by_size,get_sales_summary,get_top_revenue_products,get_top_selling_products

@tools.tool
def sales_by_brand():
    """Return total sales grouped by brand, covering all brands.
    Takes no arguments. Use for questions like 'which brand sells the most'."""
    return get_sales_by_brand()


@tools.tool
def sales_by_product():
    """Return total sales grouped by product, covering all products.
    Takes no arguments. Use for questions about how each product is selling."""
    return get_sales_by_product()


@tools.tool
def sales_by_size():
    """Return total sales grouped by product size, covering all sizes.
    Takes no arguments. Use for questions like 'which sizes sell the most'."""
    return get_sales_by_size()

    
@tools.tool
def sales_summary():
    """Return an overall summary of sales.
    Takes no arguments. Use for general questions about sales performance."""
    return get_sales_summary()

@tools.tool
def top_revenue_product():
    """Return the products that generate the highest revenue.
    Takes no arguments. Use for questions like 'which product earns the most money'."""
    return get_top_revenue_products()

@tools.tool
def top_selling_product():
    """Return the best-selling products by quantity sold.
    Takes no arguments. Use for questions like 'which product sells the most units'."""
    return get_top_selling_products()