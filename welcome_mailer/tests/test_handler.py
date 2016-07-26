from unittest import TestCase

from mandrill import InvalidKeyError

from mock import patch

from welcome_mailer import handler, models, settings
from welcome_mailer.testing_utils import fake_user_ping
from welcome_mailer.tests import fixtures


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
