from unittest import TestCase

from welcome_mailer import models
from welcome_mailer.testing_utils import create_user


class TestUserClass(TestCase):
    """ Test cases for the User class """

    def test_create(self):
        """ Test creating a new User instance.

        The constructor for the User class should accept parameters for
        first name, last name, email, time created, and time updated.
        """
        params = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'time_created': '',
            'time_updated': '',
        }

        user = models.User(**params)

        self.assertEqual(params['first_name'], user.first_name)
        self.assertEqual(params['last_name'], user.last_name)
        self.assertEqual(params['email'], user.email)
        self.assertEqual(params['time_created'], user.time_created)
        self.assertEqual(params['time_updated'], user.time_updated)

    def test_new_user_with_new_user(self):
        """ Test the is_new_user method for a new user.

        If the time_created and time_updated properties are the same,
        the method should return True.
        """
        user = create_user(time_created='time', time_updated='time')

        self.assertTrue(user.is_new_user())

    def test_new_user_with_updated_user(self):
        """ Test the is_new_user method for an updated user.

        If the time_created and time_updated properties are different,
        the method should return False.
        """
        user = create_user(time_created='time', time_updated='other time')

        self.assertFalse(user.is_new_user())

    def test_string_conversion(self):
        """ Test converting a User instance to a string.

        Converting a User instance to a string should result in a string
        formatted like "<first name> <last name>".
        """
        user = create_user()

        expected = '{} {}'.format(user.first_name, user.last_name)

        self.assertEqual(expected, str(user))

    def test_to_dict(self):
        """ Test the to_dict method of the User class.

        This method should return a dictionary with the instance's first
        name, last name, email, and is_new properties.
        """
        user = create_user()

        expected = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_new': user.is_new_user(),
        }

        self.assertEqual(expected, user.to_dict())
