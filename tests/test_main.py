from unittest import TestCase

import main
from tests import fixtures


class TestParseUser(TestCase):
    """ Test cases for the parse_user function """

    def test_parse_new_user(self):
        """ Test parsing a user from a new user event.

        If the event object is in the proper form, a User instance
        should be returned from the function.
        """
        event = fixtures.new_user_event

        user_dict = event.get('object')

        expected_kwargs = {
            'first_name': user_dict.get('userFirstName'),
            'last_name': user_dict.get('userLastName'),
            'email': user_dict.get('email'),
            'time_created': user_dict.get('createdAt'),
            'time_updated': user_dict.get('updatedAt'),
        }

        expected = main.User(**expected_kwargs)

        user = main.parse_user(event)

        self.assertEqual(expected.first_name, user.first_name)
        self.assertEqual(expected.last_name, user.last_name)
        self.assertEqual(expected.email, user.email)
        self.assertEqual(expected.time_created, user.time_created)
        self.assertEqual(expected.time_updated, user.time_updated)

    def test_parse_updated_user(self):
        """ Test parsing a user from a user update event.

        The function should be able to parse a user from the update
        event.
        """
        event = fixtures.update_user_event

        user_dict = event.get('object')

        expected_kwargs = {
            'first_name': user_dict.get('userFirstName'),
            'last_name': user_dict.get('userLastName'),
            'email': user_dict.get('email'),
            'time_created': user_dict.get('createdAt'),
            'time_updated': user_dict.get('updatedAt'),
        }

        expected = main.User(**expected_kwargs)

        user = main.parse_user(event)

        self.assertEqual(expected.first_name, user.first_name)
        self.assertEqual(expected.last_name, user.last_name)
        self.assertEqual(expected.email, user.email)
        self.assertEqual(expected.time_created, user.time_created)
        self.assertEqual(expected.time_updated, user.time_updated)
