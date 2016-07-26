import logging


class User(object):
    """ Represents a user """

    def __init__(self, first_name, last_name, email, time_created,
                 time_updated, logger=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.time_created = time_created
        self.time_updated = time_updated

        self.logger = logger or logging.getLogger(__name__)

        self.logger.debug("Created user '{}'.".format(self))

    def __eq__(self, other):
        if isinstance(other, User):
            return ((self.first_name == other.first_name) and
                    (self.last_name == other.last_name) and
                    (self.email == other.email) and
                    (self.time_created == other.time_created) and
                    (self.time_updated == other.time_updated))
        else:
            return super(User, self).__eq__(other)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        return self.__unicode__()

    def is_new_user(self):
        return self.time_created == self.time_updated

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_new': self.is_new_user(),
        }
