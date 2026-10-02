import json
import logging
from datetime import datetime, timezone

from analytics_engine.analysis import (
    product_analysis,
    purchase_analysis,
    sales_analysis,
    supplier_analysis,
)

logger = logging.getLogger(__name__)


def _safe(fn, *args, **kwargs):
    """Run one analysis; if it fails, return an error marker instead of
    crashing the whole dashboard payload."""
    try:
        return fn(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Analysis %s failed", fn.__name__)
        return {"error": f"{fn.__name__} failed: {exc}"}


def get_full_analysis(top_limit: int = 5, low_stock_threshold: int = 10) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "inventory": {
            "summary": _safe(product_analysis.get_inventory_summary),
            "low_stock": _safe(product_analysis.get_low_stock_products, low_stock_threshold),
            "out_of_stock": _safe(product_analysis.get_out_of_stock_products),
            "by_brand": _safe(product_analysis.get_products_by_brand),
            "most_expensive": _safe(product_analysis.get_most_expensive_products, top_limit),
        },
        "sales": {
            "summary": _safe(sales_analysis.get_sales_summary),
            "top_selling_products": _safe(sales_analysis.get_top_selling_products, top_limit),
            "top_revenue_products": _safe(sales_analysis.get_top_revenue_products, top_limit),
            "by_brand": _safe(sales_analysis.get_sales_by_brand),
            "by_size": _safe(sales_analysis.get_sales_by_size),
            "by_product": _safe(sales_analysis.get_sales_by_product),
        },
        "purchases": {
            "summary": _safe(purchase_analysis.get_purchase_summary),
            "top_purchased_products": _safe(purchase_analysis.get_top_purchased_products, top_limit),
            "by_supplier": _safe(purchase_analysis.get_purchases_by_supplier),
        },
        "suppliers": {
            "summary": _safe(supplier_analysis.get_supplier_summary),
        },
    }


if __name__ == "__main__":
    # Quick test:  python -m analytics_engine.analysis.main_analysis   (run from Invenship/)
    print(json.dumps(get_full_analysis(), indent=2, default=str))