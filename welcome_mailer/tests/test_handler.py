from unittest import TestCase

from mandrill import InvalidKeyError

from mock import patch

from welcome_mailer import handler, models, settings
from welcome_mailer.testing_utils import create_user
from welcome_mailer.tests import fixtures


def fake_user_ping(user_instance):
    if user_instance.master.apikey == 'invalid':
        raise InvalidKeyError('Invalid API key')

    return u'PONG!'


@patch('welcome_mailer.handler.mandrill.Users.ping', autospec=True,
       side_effect=fake_user_ping)
class TestGetClient(TestCase):
    """ Test cases for the get_client function """

    def test_get_client(self, mock_ping):
        """ Test getting the mandrill client.

        The client should get the API_KEY from the settings file.
        """
        client = handler.get_client()

        self.assertEqual(settings.API_KEY, client.apikey)
        self.assertEqual(1, mock_ping.call_count)

    @patch('welcome_mailer.handler.settings.API_KEY', 'invalid')
    def test_invalid_key(self, mock_ping):
        """ Test using an invalid api key.

        If the api key is invalid, and InvalidKeyError should be raised.
        """
        with self.assertRaises(InvalidKeyError):
            handler.get_client()

        self.assertEqual(1, mock_ping.call_count)


@patch('welcome_mailer.handler.send_email', autospec=True, return_value={})
class TestLambdaHandler(TestCase):
    """ Test cases for the lambda_handler function """

    def test_new_user(self, mock_send_email):
        """ Test sending a new user event to the handler.

        If a new user event is sent to the handler, an email should be
        sent to the new user.
        """
        event = fixtures.new_user_event
        user = models.User.from_event(event)

        result = handler.lambda_handler(event, None)

        self.assertEqual({}, result)
        mock_send_email.assert_called_with(user)

    def test_update(self, mock_send_email):
        """ Test sending an update event to the handler.

        If the event is a user being updated, no mail should be sent,
        and a blank dictionary should be returned.
        """
        event = fixtures.update_user_event

        result = handler.lambda_handler(event, None)

        self.assertEqual({}, result)
        self.assertEqual(0, mock_send_email.call_count)


@patch('welcome_mailer.handler.mandrill.Messages.send_template')
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

        handler.send_email(user)

        mock_send_template.assert_called_with(
            template_name=template_name,
            template_content=template_content,
            message=message)
