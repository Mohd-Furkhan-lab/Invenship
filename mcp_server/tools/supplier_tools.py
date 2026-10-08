from mcp_server.mcp import tools
from analytics_engine.analysis.supplier_analysis import get_supplier_summary

@tools.tool
def supplier_summary():
    return get_supplier_summary()

