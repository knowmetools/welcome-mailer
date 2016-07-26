from welcome_mailer import models


DEFAULT_USER_PARAMS = {
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'test@example.com',
    'time_created': '',
    'time_updated': '',
}


def create_user(**kwargs):
    """ Create a user with defaults for testing """
    params = {}

    for key in DEFAULT_USER_PARAMS.keys():
        if key in kwargs:
            params[key] = kwargs.pop(key)
        else:
            params[key] = DEFAULT_USER_PARAMS.get(key)

    if kwargs:
        raise ValueError("Received unexpected kwargs: %s" % kwargs)

    return models.User(**params)
