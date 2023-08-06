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
order_fields = [
    "id",
    "myshopify_name",
    "status",
    "financial_status",
    "fulfillment_status",
    "email",
    "closed_at",
    "number",
    "note",
    "token",
    "gateway",
    "test",
    "total_price",
    "subtotal_price",
    "total_tax",
    "taxes_included",
    "currency",
    "confirmed",
    "total_discounts",
    "total_line_items_price",
    "cart_token",
    "buyer_accepts_marketing",
    "name",
    "referring_site",
    "landing_site",
    "cancelled_at",
    "cancel_reason",
    "total_price_usd",
    "checkout_token",
    "reference",
    "user_id",
    "location_id",
    "source_identifier",
    "source_url",
    "processed_at",
    "device_id",
    "phone",
    "customer_locale",
    "app_id",
    "browser_ip",
    "landing_site_ref",
    "order_number",
    "processing_method",
    "checkout_id",
    "source_name",
    "tags",
    "contact_email",
    "order_status_url",
    "presentment_currency",
    "json"]


order_line_fields = [
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
    "",
    "fulfillable_quantity",
    "grams",
    "price",
    "total_discount",
    "fulfillment_status",
    "admin_graphql_api_id",
    "json"]


product_fields = [
    "id",
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
# fmt:on

order_dict_default = {}
order_line_dict_default = {}
product_dict_default = {}

for f in order_fields:
    order_dict_default[f] = None

for f in order_line_fields:
    order_line_dict_default[f] = None

for f in product_fields:
    product_dict_default[f] = None


def images_to_image_src(images):
    if not images or len(images) < 1:
        logger.warning("Error in retrieved product images")
        return "https://fk.z5.no/static/images/favicon.png"
    image = images.pop()
    if not image or not image.src:
        logger.warning("Error in retrieved product image")
        return "https://fk.z5.no/static/images/favicon.png"
    return image.src


def salespop_order_from_order(order_dict, order_line_dict, product):
    customer = order_dict.get("customer", {})
    default_address = customer.get("default_address", {})

    product_url = f"https://{order_dict.get('myshopify_name')}/products/{product.handle}"
    image_src = images_to_image_src(product.images)

    salespop_order = {"order_id": order_dict.get("id"), "order_line_id": order_line_dict.get("id"), "myshopify_name": order_dict.get("myshopify_name"), "product_title": order_line_dict.get("title"), "product_quantity": order_line_dict.get("quantity"), "product_variant_title": order_line_dict.get("variant_title"), "product_vendor": order_line_dict.get("vendor"), "product_price": order_line_dict.get("price"), "product_total_discount": order_line_dict.get("total_discount"), "product_image_url": image_src, "product_url": product_url, "customer_first_name": default_address.get("first_name"), "customer_last_name": default_address.get("last_name"), "customer_city": default_address.get("city"), "customer_country": default_address.get("country"), "customer_country_code": default_address.get("country_code"), "closed_at": order_dict.get("created_at")}
    return salespop_order


def put_batch_job_fetch_product(config, shop_domain, product_id):
    id = False
    if not shop_domain:
        raise Exception("No shop_doamin")
    try:
        bp = fk.batch.BatchProcessor.BatchProcessor(config)
        id = bp.insert_batch_item(type="shopify-products-fetch", data=json.dumps({"shop_domain": shop_domain, "product_id": product_id}), priority=50, source=None) or False
    except Exception as e:
        logger.error(f"Could not submit batch job to fetch product {product_id}: {e}", exc_info=True)
    return id


def batch_filter_entrypoint(batch_item={}, config={}):
    # logger.info(f"SHOPIFY ORDERS FETCH RUNNING WITH {batch_item} ######################")
    data = json.loads(batch_item.get("data", {}))
    if not data:
        return None, "No data"
    shop_domain = data.get("shop_domain")
    if not shop_domain:
        return None, "No shop domain"
    order_id = data.get("order_id")
    if not order_id:
        return None, "No order_id"
    shop_domain = shop_domain.strip()
    db = Database(config)  # No flask context: get_flask_shopify_db(config)
    shop = db.get_shop(shop_domain)
    if not shop:
        return None, "No shop"
    token = shop.get("offline_access_token", None)
    if not token:
        return None, "No token"
    # logger.info(f"TOKEN FROM DB WAS: {token}")
    sm = ShopifySessionManager(config=config, db=db, shop_domain=shop_domain, token=token)
    # sm.self_install()
    order_dict_raw = sm.get_order_by_id(order_id)
    # logger.warning(pprint.pformat(orders))
    if not order_dict_raw:
        return None, "No order"
    # logger.info(f" + ORDER: {order}")
    order_dict = {**order_dict_default, **order_dict_raw}
    # Augment it with some needed extras
    order_dict["myshopify_name"] = shop_domain
    order_dict["json"] = json.dumps(order_dict, indent=3, sort_keys=True)
    # j=json.dumps(order_dict, indent=3, sort_keys=True)
    order_id = db.upsert_order(order_dict)
    if not order_id:
        return None, "Could not upsert order"
    order_lines = order_dict.get("line_items", [])
    for order_line_dict_raw in order_lines:
        order_line_dict = {**order_line_dict_default, **order_line_dict_raw}
        order_line_dict["order_id"] = order_id
        order_line_dict["myshopify_name"] = shop_domain
        order_line_dict["json"] = json.dumps(order_line_dict, indent=3, sort_keys=True)
        # Just put intermediate version of the product here to ensure our foreign key constraint will be met
        product_id = order_line_dict["product_id"]
        product_dict = {**product_dict_default}
        product_dict["id"] = product_id
        product_dict["myshopify_name"] = shop_domain
        # , **{"id": product_id, "myshopify_name": shop_domain}}
        id = db.upsert_product(product_dict)
        if product_id != id:
            logger.warning(f"Could not insert preliminary product for order line with product_id {product_id}, skipping order line...")
            continue
        order_line_id = db.upsert_order_line(order_line_dict)
        if not order_line_id:
            return None, "Could not save order line"
        job_id = put_batch_job_fetch_product(config, shop_domain, product_id)
        if not job_id:
            return None, f"Could not put fetch product job for {product_id}"
        # product_variants_dict["inventory_quantity"] = int(float(product_dict.get("inventory_quantity", "0")))
        # db.upsert_product_variants(product_variants_dict)
        # product = sm.get_product_by_id(product_variants_dict["product_id"])

        # Phasint out the simplified table for now
        # salespop_order_dict = salespop_order_from_order(order_dict, order_line_dict, product)
        # db.upsert_salespop_order(salespop_order_dict)
        # db.update_shop_orders_updated_at(shop_domain)
    return None, None
