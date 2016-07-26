from unittest import TestCase

from mock import patch

from welcome_mailer import handler, models
from welcome_mailer.tests import fixtures


@patch('welcome_mailer.handler.MandrillBackend.send_email', return_value={})
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
