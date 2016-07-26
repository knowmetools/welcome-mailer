#! /usr/bin/env python

from __future__ import print_function

import logging
import sys

import mandrill

from welcome_mailer import models, settings


VERSION = '1.0.0'


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)8s - %(message)s')

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)

logger.addHandler(sh)


def get_client():
    """ Get mandrill client """
    return mandrill.Mandrill(settings.API_KEY)


def lambda_handler(event, context):
    """ Handle main lambda event """
    logger.debug("Received event: %s" % event)

    user = models.User.from_event(event)

    logger.debug("Parsed user: %s" % user)

    user_dict = user.to_dict()

    logger.debug("User dict: %s" % user_dict)

    if user.is_new_user():
        logger.debug("Sending email to new user.")

        results = send_email(user)

        logger.debug("Results: %s" % results)
    else:
        results = {}

    return results


def send_email(user):
    """ Send greeting email to user """
    client = get_client()

    template_name = settings.TEMPLATE_NAME
    template_content = []
    message = {
        'from_email': 'no-reply@knowmetools.com',
        'global_merge_vars': [
            {
                'name': 'COMPANY',
                'content': 'Know Me, LLC',
            },
            {
                'name': 'LIST_ADDRESS_HTML',
                'content': settings.ADDRESS_HTML,
            },
        ],
        'merge_language': 'mailchimp',
        'to': [
            {
                'email': user.email,
                'name': str(user),
            },
        ],
    }

    return client.messages.send_template(
        template_name=template_name, template_content=template_content,
        message=message)
