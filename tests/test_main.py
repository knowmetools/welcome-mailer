from unittest import TestCase

from mock import patch

import local_settings as settings
import main
from testing_utils import create_user
from tests import fixtures


class TestGetClient(TestCase):
    """ Test cases for the get_client function """

    def test_get_client(self):
        """ Test getting the mandrill client.

        The client should get the API_KEY from the settings file.
        """
        client = main.get_client()

        self.assertEqual(settings.API_KEY, client.apikey)


@patch('main.send_email', autospec=True, return_value={})
class TestLambdaHandler(TestCase):
    """ Test cases for the lambda_handler function """

    def test_new_user(self, mock_send_email):
        """ Test sending a new user event to the handler.

        If a new user event is sent to the handler, an email should be
        sent to the new user.
        """
        event = fixtures.new_user_event
        user = main.parse_user(event)

        result = main.lambda_handler(event, None)

        self.assertEqual({}, result)
        mock_send_email.assert_called_with(user)

    def test_update(self, mock_send_email):
        """ Test sending an update event to the handler.

        If the event is a user being updated, no mail should be sent,
        and a blank dictionary should be returned.
        """
        event = fixtures.update_user_event

        result = main.lambda_handler(event, None)

        self.assertEqual({}, result)
        self.assertEqual(0, mock_send_email.call_count)


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


@patch('main.mandrill.Messages.send_template')
class TestSendEmail(TestCase):
    """ Test cases for the send_email function """

    def test_send_email(self, mock_send_template):
        """ Test sending an email to a user.

        The function should attempt to send a templated email using
        mandrill.
        """
        user = create_user(email='test@example.com')

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

        main.send_email(user)

        mock_send_template.assert_called_with(
            template_name=template_name,
            template_content=template_content,
            message=message)


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

        user = main.User(**params)

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
