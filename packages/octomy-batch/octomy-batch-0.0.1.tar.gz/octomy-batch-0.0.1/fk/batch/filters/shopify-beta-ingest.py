import pprint
import time
import random
import logging
import re
import json
import requests
from validate_email import validate_email
from urllib.parse import urlparse
import fk.utils
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


def verify_website(url):
    return bool(requests.get(url))


def shopify_domain_for_url(url):
    myshopify_domain = None
    rex = "([0-9a-z\-_]{1,20}\.myshopify\.com)"
    # If the url is on the myshopify form already, go at it directly
    if not url:
        return None, "No url"
    if ".myshopify.com" in url:
        m = re.search(rex, url)
        myshopify_domain = m.group(0)
    elif url.startsWith("http://") or url.startsWith("https://"):
        parts = urlparse(url)
        canonical_url = f"{parts['scheme']}://{parts['hostname']}"
        r = requests.get(canonical_url)
        if r:
            m = re.search(rex, r.body)
            myshopify_domain = m.group(0)
        else:
            return None, f"Could not fetch canonical URL: '{canonical_url}' for '{url}'"
    if myshopify_domain:
        if verify_website(f"https://{url}"):
            return myshopify_domain, None
        else:
            return None, f"Invalid myshopify_domain found: {myshopify_domain}"
    else:
        return None, f"No myshopify_domain found: {myshopify_domain}"
    return None, "Unknown error"


def prepare_email(sender, receiver, subject, body, body_html):
    # Create message container - the correct MIME type is multipart/alternative here!
    msg = MIMEMultipart("alternative")
    msg["subject"] = subject
    msg["To"] = receiver
    msg["From"] = sender
    msg.preamble = body
    msg.attach(MIMEText(body_html, "html"))
    return msg.as_string()


def batch_filter_entrypoint(batch_item={}, config={}):
    data_str = batch_item.get("data", "")
    # logger.info(f"SHOPIFY BETA INGEST RUNNING WITH {data_str} ######################")
    data = {}
    try:
        data = json.loads(data_str)
    except Exception as e:
        return None, f"Could not parse json: {data_str}"
    receiver = data.get("email")
    shop_url = data.get("shop_url")
    myshopify_domain, myshopify_error = shopify_domain_for_url(shop_url)
    if not myshopify_domain:
        return None, myshopify_error or "Unknown error"
    if not validate_email(receiver, check_mx=True, verify=True):
        return None, f"Email invalid: '{receiver}'"
    domain = config.get("email-domain")
    user = config.get("email-user")
    sender = f"{user}@{domain}"
    password = config.get("email-password")
    nonce = fk.utils.random_str(32)
    try:
        with smtplib.SMTP("postfix") as smtp:
            body_template = """This is an autoamted  message to confirm that your FirstKiss Salespop BETA submission was accepted.\r\n\r\n
To start installation, please click the link:\r\n
https://{myshopify_domain}/admin?nonce={nonce}
"""
            body_html_template = """
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>FirstKiss Salespop BETA submission</title>
<style type="text/css" media="screen">
*{{
    font-family:sans;
}}
</style>
<h1>Congratulations!</h1>
<p>This is autoamted message is a confirmation that your FirstKiss Salespop BETA submission was accepted!\n
To start installation, please click the link:</p>
<br/>
<a href="https://{myshopify_domain}/admin?nonce={nonce}">install FirstKiss Salespop</a>
"""
            try:
                # logger.info(f"Logging into '{sender}' with '{password}'")
                smtp.login(sender, password)
            except Exception as e:
                return None, f"Error logging into email server: {e}"
            try:
                body = body_template.format(sender=sender, receiver=receiver, myshopify_domain=myshopify_domain, nonce=nonce)
                body_html = body_html_template.format(sender=sender, receiver=receiver, myshopify_domain=myshopify_domain, nonce=nonce)
                subject = f"BETA confirmation for {myshopify_domain}"
                message = prepare_email(sender=sender, receiver=receiver, subject=subject, body=body, body_html=body_html)
                # logger.info(f"Sending message '{message}' from '{sender}' to '{receiver}'")
                smtp.sendmail(sender, receiver, message)
            except Exception as e:
                return None, f"Error sending email: {e}"
    except Exception as e:
        return None, f"Error with email sending: {e}"
    return None, None
