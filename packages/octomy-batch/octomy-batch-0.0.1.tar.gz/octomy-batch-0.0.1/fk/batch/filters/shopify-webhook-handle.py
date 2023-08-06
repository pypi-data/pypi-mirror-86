import logging

from fk.api.shopify import ShopifySessionManager
from fk.api.shopify.db import Database, get_flask_shopify_db

import json

logger = logging.getLogger(__name__)


def batch_filter_entrypoint(batch_item={}, config={}):
    # logger.info(f"SHOPIFY ORDERS FETCH RUNNING WITH {batch_item} ######################")
    data = json.loads(batch_item.get("data", {}))
    if not data:
        return None, "No data"
    shop_domain = data.get("shop_domain")
    if not shop_domain:
        return None, "No shop domain"
    topic = data.get("topic")
    if not order_id:
        return None, "No topic"
    shop_domain = shop_domain.strip()
    logger.info(f"Effectively aknowleging webhook of topic {topic} for {shop_domain}")
    return None, None
