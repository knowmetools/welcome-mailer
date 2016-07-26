from __future__ import print_function

import logging
from logging.config import dictConfig

import mandrill

from welcome_mailer import models, settings


dictConfig(settings.LOGGING_CONFIG)


def get_client():
    """ Get mandrill client """
    return mandrill.Mandrill(settings.API_KEY)


def lambda_handler(event, context, logger=None):
    """ Handle main lambda event """
    logger = logger or logging.getLogger(__name__)

    logger.debug("Received event: %s" % event)

    user = models.User.from_event(event)

    if user.is_new_user():
        results = send_email(user)

        logger.info("Sent welcome email to {}".format(user.email))
        logger.debug("Results: %s" % results)
    else:
        results = {}

        logger.info("Did not send email to updated user {}".format(user.email))

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
