import sys
from mcp_server.app import tools
from mcp_server.tools import sales_tools, product_tools, purchase_tools, supplier_tools

if __name__ == "__main__":
    if "--http" in sys.argv:
        tools.run(transport="streamable-http", host="127.0.0.1", port=8001)
    else:
        tools.run() 