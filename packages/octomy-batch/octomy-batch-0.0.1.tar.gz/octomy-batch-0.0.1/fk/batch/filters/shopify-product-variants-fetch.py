import logging

from fk.api.shopify import ShopifySessionManager
from fk.api.shopify.db import Database, get_flask_shopify_db

# from fk.api.shopify.Database import *
import pprint
import time
import random
import json

logger = logging.getLogger(__name__)

# fmt:off

product_variant_fields = ["id",
    "product_id",
    "title",
    "price",
    "sku",
    "position",
    "inventory_policy",
    "compare_at_price",
    "fulfillment_service",
    "inventory_management",
    "option1",
    "option2",
    "option3",
    "taxable",
    "barcode",
    "grams",
    "image_id",
    "weight",
    "weight_unit",
    "inventory_item_id",
    "inventory_quantity",
    "old_inventory_quantity",
    "requires_shipping",
    "admin_graphql_api_id",
    "json"]
# fmt:on


product_variant_dict_default = {}

for f in product_variant_fields:
    product_variant_dict_default[f] = None


def batch_filter_entrypoint(batch_item={}, config={}):
    # logger.info(f"SHOPIFY PRODUCTS FETCH RUNNING WITH {batch_item} ######################")
    data = json.loads(batch_item.get("data", {}))
    if not data:
        return None, "No data"
    shop_domain = data.get("shop_domain")
    if not shop_domain:
        return None, "No shop url"
    product_variant_id = data.get("product_variant_id")
    if not product_variant_id:
        return None, "No product_variant_id"
    product_id = data.get("product_id")
    if not product_id:
        return None, "No product_id"
    shop_domain = shop_domain.strip()
    db = Database(config)  # No flask context: get_flask_shopify_db(config)
    shop = db.get_shop(shop_domain)
    if not shop:
        return None, "No shop"
    token = shop.get("offline_access_token", None)
    if not token:
        return None, "No token"
    sm = ShopifySessionManager(config=config, db=db, shop_domain=shop_domain, token=token)
    product_variant = sm.get_product_variant_by_id(product_id, product_variant_id)
    # logger.warning(pprint.pformat(product_variant))
    if not product_variant:
        return None, "No product_variant"
    product_variant_dict_raw = product_variant.to_dict()
    product_variant_dict = {**product_variant_dict_default, **product_variant_dict_raw}
    if product_variant_dict["id"] != product_variant_id:
        return None, f"Returned product_variant {product_variant_dict['id']} did not match initial id {product_variant_id}"
    # Augment it with some needed extras
    product_variant_dict["myshopify_name"] = shop_domain
    product_variant_dict["json"] = json.dumps(product_variant_dict, indent=3, sort_keys=True)
    product_variant_id = db.upsert_product_variant(product_variant_dict)
    if not product_variant_id:
        return None, "Could not save product_variant"
    return None, None
