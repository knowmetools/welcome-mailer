from __future__ import print_function

import logging
from logging.config import dictConfig

from welcome_mailer import models, settings
from welcome_mailer.backends.email import MandrillBackend


dictConfig(settings.LOGGING_CONFIG)


def lambda_handler(event, context, logger=None):
    """ Handle main lambda event """
    logger = logger or logging.getLogger(__name__)

    logger.debug("Received event: %s" % event)

    user = models.User.from_event(event)

    if user.is_new_user():
        backend = MandrillBackend(settings.API_KEY)

        results = backend.send_email(user)

        logger.info("Sent welcome email to {}".format(user.email))
        logger.debug("Results: %s" % results)
    else:
        results = {}

        logger.info("Did not send email to updated user {}".format(user.email))

    return results
