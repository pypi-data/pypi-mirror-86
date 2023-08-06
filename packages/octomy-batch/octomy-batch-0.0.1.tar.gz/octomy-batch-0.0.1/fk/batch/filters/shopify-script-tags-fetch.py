import logging

# from flask import url_for

from fk.api.shopify import ShopifySessionManager
from fk.api.shopify.db import Database

import json

logger = logging.getLogger(__name__)


def batch_filter_entrypoint(batch_item={}, config={}):
    # logger.info(f"SHOPIFY PRODUCTS FETCH RUNNING WITH {batch_item} ######################")
    data = json.loads(batch_item.get("data", {}))
    shop_domain = data.get("shop_domain")
    shop_domain = shop_domain.strip()
    if not shop_domain:
        return None, "No shop_domain"
    db = Database(config)  # No flask context: get_flask_shopify_db(config)
    sm = ShopifySessionManager(config=config, db=db, shop_domain=shop_domain)
    si_ok, si_msg = sm.self_install()
    if not si_ok:
        return None, f"Could not self install session manager: {si_msg}"

    # shop = db.get_shop(shop_domain)
    # if not shop:
    #    return None, "No shop"
    # token = shop.get("offline_access_token", None)
    # if not token:
    #    return None, "No token"
    # sm = ShopifySessionManager(config=config, db=db, shop_domain=shop_domain, token=token)
    auth_ok, auth_error = sm.is_authenticated()
    if not auth_ok:
        return None, f"Could not authenticate: {auth_error}"
    script_tag_url = "https://test.merchbot.net/shopify/script_tag"
    # url_for("shopify_spop_bp.script_tag", _external=True)
    logger.info(f"Using script_tag_url='{script_tag_url}'")
    script_tags = sm.get_script_tags(script_tag_url)
    return f"RES: {script_tags}", None


"""
Error creating session with api_url=https://bonkers-test-store.myshopify.com/admin/api/2020-04,
token='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',
shop_domain=bonkers-test-store.myshopify.com,
api-version=2020-04:
    
Response(code=401,
body="b'{"errors":"[API] Invalid API key or access token (unrecognized login or wrong password)"}'", headers={'Date': 'Sun, 27 Sep 2020 23:28:06 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'close', 'Set-Cookie': '__cfduid=da3693a61939439155461ca47f9e418f21601249285; expires=Tue, 27-Oct-20 23:28:05 GMT; path=/; domain=.myshopify.com; HttpOnly; SameSite=Lax', 'X-Sorting-Hat-PodId': '34', 'X-Sorting-Hat-ShopId': '5263130659', 'Referrer-Policy': 'origin-when-cross-origin', 'X-Frame-Options': 'DENY', 'X-ShopId': '5263130659', 'X-ShardId': '34', 'WWW-Authenticate': 'Basic Realm="Shopify API Authentication"', 'Strict-Transport-Security': 'max-age=7889238', 'X-Shopify-Stage': 'production', 'Content-Security-Policy': "default-src 'self' data: blob: 'unsafe-inline' 'unsafe-eval' https://* shopify-pos://*; block-all-mixed-content; child-src 'self' https://* shopify-pos://*; connect-src 'self' wss://* https://*; frame-ancestors 'none'; img-src 'self' data: blob: https:; script-src https://cdn.shopify.com https://cdn.shopifycdn.net https://checkout.us.shopifycs.com https://js-agent.newrelic.com https://bam.nr-data.net https://api.stripe.com https://mpsnare.iesnare.com https://appcenter.intuit.com https://www.paypal.com https://js.braintreegateway.com https://c.paypal.com https://maps.googleapis.com https://www.google-analytics.com https://v.shopify.com https://widget.intercom.io https://js.intercomcdn.com 'self' 'unsafe-inline' 'unsafe-eval'; upgrade-insecure-requests; report-uri /csp-report?source%5Baction%5D=show&source%5Bapp%5D=Shopify&source%5Bcontroller%5D=admin%2Fshops&source%5Bsection%5D=admin_api&source%5Buuid%5D=92d591f5-b7a3-49f0-8ac0-e603429b167c", 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-XSS-Protection': '1; mode=block; report=/xss-report?source%5Baction%5D=show&source%5Bapp%5D=Shopify&source%5Bcontroller%5D=admin%2Fshops&source%5Bsection%5D=admin_api&source%5Buuid%5D=92d591f5-b7a3-49f0-8ac0-e603429b167c', 'X-Dc': 'gcp-us-central1,gcp-us-east1,gcp-us-east1', 'X-Request-ID': '92d591f5-b7a3-49f0-8ac0-e603429b167c', 'CF-Cache-Status': 'DYNAMIC', 'cf-request-id': '05737e2ed30000ec7a8dbf9200000001', 'Expect-CT': 'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"', 'Server': 'cloudflare', 'CF-RAY': '5d98ffc48e6cec7a-DFW', 'alt-svc': 'h3-27=":443"; ma=86400, h3-28=":443"; ma=86400, h3-29=":443"; ma=86400'}, msg="Unauthorized")
2020-09-27 23:28:06 INFO (MainThread) [pyactiveresource.connection:257::_open()] - GET https://bonkers-test-store.myshopify.com/admin/api/2020-04/products/123.json
"""
