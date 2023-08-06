import logging

from fk.api.shopify import ShopifySessionManager
from fk.api.shopify.db import Database, get_flask_shopify_db
import fk.batch.BatchProcessor

# from fk.api.shopify.Database import *
import pprint
import time
import random
import json

logger = logging.getLogger(__name__)

# fmt:off
product_fields = [
    "id",
    "myshopify_name",
    "handle",
    "body_html",
    "options",
    "product_type",
    "published_at",
    "published_scope",
    "tags",
    "template_suffix",
    "title",
    "variants",
    "vendor",
    "json"]

product_variants_fields = [
    "id",
    "myshopify_name",
    "variant_id",
    "title",
    "quantity",
    "sku",
    "variant_title",
    "vendor",
    "fulfillment_service",
    "product_id",
    "requires_shipping",
    "taxable",
    "gift_card",
    "name",
    "variant_inventory_management",
    "product_exists",
    "fulfillable_quantity",
    "grams",
    "price",
    "total_discount",
    "fulfillment_status",
    "admin_graphql_api_id",
    "json"]
# fmt:on

product_dict_default = {}
product_variants_dict_default = {}

for f in product_fields:
    product_dict_default[f] = None

for f in product_variants_fields:
    product_variants_dict_default[f] = None


def put_batch_job_fetch_product_variant(config, shop_domain, product_id, product_variant_id):
    id = False
    try:
        bp = fk.batch.BatchProcessor.BatchProcessor(config)
        id = bp.insert_batch_item(type="shopify-product-variants-fetch", data=json.dumps({"shop_domain": shop_domain, "product_id": product_id, "product_variant_id": product_variant_id}), priority=50, source=None) or False
    except Exception as e:
        logger.error(f"Could not submit batch job fetch product {product_id} variant {product_variant_id}: {e}", exc_info=True)
    return id


def batch_filter_entrypoint(batch_item={}, config={}):
    # logger.info(f"SHOPIFY PRODUCTS FETCH RUNNING WITH {batch_item} ######################")
    data = json.loads(batch_item.get("data", {}))
    shop_domain = data.get("shop_domain")
    product_id = data.get("product_id")
    if not shop_domain:
        return None, "No shop_domain"
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
    product = sm.get_product_by_id(product_id)
    # logger.warning(pprint.pformat(product))
    if not product:
        return None, "No product"
    product_dict_raw = product.to_dict()
    product_dict = {**product_dict_default, **product_dict_raw}
    if product_dict["id"] != product_id:
        return None, f"Returned product {product_dict['id']} did not match initial id {product_id}"
    # Augment it with some needed extras
    product_dict["myshopify_name"] = shop_domain
    product_dict["json"] = json.dumps(product_dict, indent=3, sort_keys=True)
    product_dict["options"] = json.dumps(product_dict["options"], indent=3, sort_keys=True)
    product_dict["variants"] = json.dumps(product_dict["variants"], indent=3, sort_keys=True)
    # logger.warning(pprint.pformat(product_dict["variants"]))
    id = db.upsert_product(product_dict)
    if not id:
        return None, "Could not save product"
    if id != product_id:
        return None, f"Saved id {id} was different from original id {product_id}"
    product_variants = json.loads(product_dict.get("variants", "[]"))
    for product_variants_dict_raw in product_variants:
        product_variant_id = product_variants_dict_raw.get("id")
        if not product_variant_id:
            return None, "No product_variant_id"
        job_id = put_batch_job_fetch_product_variant(config, shop_domain, product_id, product_variant_id)
        if not job_id:
            return None, f"Could not put fetch product variant job for {product_id}"
    return None, None
