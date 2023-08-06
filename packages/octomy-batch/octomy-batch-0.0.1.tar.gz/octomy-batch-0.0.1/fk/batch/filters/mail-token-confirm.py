import pprint
import time
import random
import logging

from smtplib import SMTP

logger = logging.getLogger(__name__)


def batch_filter_entrypoint(batch_item={}, config={}):
    data = batch_item.get("data", "data-field-missing")
    logger.info(f"MAIL TOKEN CONFIRM RUNNING WITH {data} ######################")
    domain = config.get("email-domain")
    user = config.get("email-user")
    password = config.get("email-password")
    sender = f"{user}@{domain}"
    receivers = ["test-spam@octomy.org"]
    message_template = """From: First Kiss <{0}>
To: <{1}>
Subject: Hello 
This is a test"""
    with SMTP("postfix") as smtp:
        smtp.login(sender, password)
        for receiver in receivers:
            logger.info(f"Sending email from{sender} to {receiver}")
            smtp.sendmail(sender, receiver, message_template.format(sender, receiver))
