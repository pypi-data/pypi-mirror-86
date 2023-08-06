import logging

from fk.api.shopify.db import Database as ShopifyDB

import fk.batch.BatchProcessor
import datetime

logger = logging.getLogger(__name__)


def batch_filter_entrypoint(batch_item={}, config={}):
    # logger.info(f"SHOPIFY ORDERS FETCH ALL RUNNING WITH {batch_item} ######################")
    db = ShopifyDB(config)
    shops = db.get_shop_names()
    if not shops:
        logger.error(f"No shops")
        return None, None
    bp = fk.batch.BatchProcessor.BatchProcessor(config)
    min_mean = datetime.timedelta(hours=1)
    for shop in shops:
        shop_name = shop.get("myshopify_name", None)
        if not shop_name:
            logger.error(f"No shop name, skipping")
            continue
        count = shop.get("count", 0)
        if not count:
            # logger.warning(f"Count was <1 for shop {shop_name}, skipping")
            continue
        # Calculate if shop is active enough to warrant a new fetch
        interval = shop.get("interval", datetime.timedelta(days=0))
        if not interval:
            logger.error(f"Invalid interval: '{interval}' for shop {shop_name}, skipping")
            continue
        mean_time = shop.get("interval_per_count", datetime.timedelta(days=0))
        if not mean_time:
            logger.error(f"Invalid mean_time: '{mean_time}' for shop {shop_name}, skipping")
            continue
        # count = shop.get("count", 0) logger.info(f"## SHOP: {shop} ct={count} iv={interval} mean={mean_time} min={min_mean}")
        if mean_time < min_mean or interval > min_mean:
            # logger.info("---------------------------------------------------------------")
            try:
                id = bp.insert_batch_item(type="shopify-orders-fetch", data=shop_name, priority=50, source=None) or -1
            except Exception as e:
                logger.error(f"Could not submit batch item", exc_info=True)
    return None, None
