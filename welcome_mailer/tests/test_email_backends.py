from unittest import TestCase

from mandrill import InvalidKeyError

from mock import patch

from welcome_mailer import settings
from welcome_mailer.backends import email
from welcome_mailer.testing_utils import create_user, fake_user_ping


class TestBaseBackend(TestCase):
    """ Test cases for the base email backend """

    def test_send_email(self):
        """ Test sending an email with the base backend.

        Sending an email with this backend should raise a
        NotImplementedError.
        """
        backend = email.BaseBackend()
        user = create_user()

        with self.assertRaises(NotImplementedError):
            backend.send_email(user)


@patch('welcome_mailer.backends.email.mandrill_backend.mandrill.Users.ping',
       autospec=True, side_effect=fake_user_ping)
class TestMandrillBackend(TestCase):
    """ Test cases for the mandrill email backend """

    def test_create(self, mock_ping):
        """ Test creating a mandrill backend.

        The mandrill backend should accept an API key in its
        constructor.
        """
        backend = email.MandrillBackend('apikey')

        self.assertFalse(backend.authenticated)

        # ping shouldn't be called until we actually try to send an
        # email.
        self.assertEqual(0, mock_ping.call_count)

    def test_authenticate(self, mock_ping):
        """ Test authenticating the backend.

        This method should send a ping through mandrill to determine if
        the API key is valid.
        """
        backend = email.MandrillBackend('apikey')
        backend.authenticate()

        self.assertTrue(backend.authenticated)
        self.assertEqual(1, mock_ping.call_count)

    def test_authenticate_already_authenticated(self, mock_ping):
        """ Test authenticating when already authenticated.

        If the backend is already authenticated, then the API should not
        be hit again.
        """
        backend = email.MandrillBackend('apikey')
        backend.authenticated = True

        backend.authenticate()

        self.assertTrue(backend.authenticated)
        self.assertEqual(0, mock_ping.call_count)

    def test_authenticate_invalid_key(self, mock_ping):
        """ Test authenticating with an invalid key.

        Attempting to authenticate an invalid key should raise an
        InvalidKeyError.
        """
        backend = email.MandrillBackend('invalid')

        with self.assertRaises(InvalidKeyError):
            backend.authenticate()

        self.assertFalse(backend.authenticated)
        self.assertEqual(1, mock_ping.call_count)

    def test_get_message(self, mock_ping):
        """ Test getting the message content for a user.

        This method should generate the message content for a welcome
        email to a specific user. It should pull in global variables
        from settings, and generate personal variables for the current
        user.
        """
        backend = email.MandrillBackend('apikey')
        user = create_user()

        expected = settings.MESSAGE_CONFIG
        expected.update({
            'to': [
                {
                    'email': user.email,
                    'name': str(user),
                },
            ],
        })

        self.assertEqual(expected, backend.get_message(user))

    @patch('welcome_mailer.backends.email.mandrill_backend.mandrill.Messages.send_template',        # noqa
           return_value={})
    def test_send_email(self, mock_send_template, mock_ping):
        """ Test sending an email to a user.

        The function should attempt to send a templated email using
        mandrill.
        """
        backend = email.MandrillBackend('apikey')
        user = create_user(email='test@example.com')

        template_name = settings.TEMPLATE_NAME
        template_content = []
        message = backend.get_message(user)

        backend.send_email(user)

        self.assertEqual(1, mock_ping.call_count)
        mock_send_template.assert_called_with(
            template_name=template_name,
            template_content=template_content,
            message=message)
