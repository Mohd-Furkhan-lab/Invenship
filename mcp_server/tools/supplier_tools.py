from mcp_server.mcp import tools
from analytics_engine.analysis.supplier_analysis import get_supplier_summary

@tools.tool
def supplier_summary():
    """Return an overall summary of all suppliers.
    Takes no arguments. Use for general questions about suppliers."""
    return get_supplier_summary()