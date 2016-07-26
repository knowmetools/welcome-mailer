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

    @classmethod
    def from_event(cls, event, logger=None):
        """ Parse a user from an event """
        logger = logger or logging.getLogger(__name__)

        user_dict = event.get('object')

        logger.debug("Parsing user from: {}".format(user_dict))

        first_name = user_dict.get('userFirstName')
        last_name = user_dict.get('userLastName')
        email = user_dict.get('email')
        time_created = user_dict.get('createdAt')
        time_updated = user_dict.get('updatedAt')

        return cls(first_name, last_name, email, time_created, time_updated)

    def is_new_user(self):
        return self.time_created == self.time_updated

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_new': self.is_new_user(),
        }
