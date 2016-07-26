import logging


class BaseBackend(object):
    """ Base backend for all email backends """

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def send_email(self, user):
        """ Should be implemented by a subclass """
        raise NotImplementedError(
            "This method should be implemented by a subclass")
