import mandrill

from welcome_mailer import settings
from welcome_mailer.backends.email import BaseBackend


class MandrillBackend(BaseBackend):
    """ Backend for sending user emails through mandrill """

    def __init__(self, api_key, *args, **kwargs):
        super(MandrillBackend, self).__init__(*args, **kwargs)

        self.client = mandrill.Mandrill(api_key)

        self.authenticated = False

    def authenticate(self):
        """ Authenticate the backend by pinging the mandrill API """

        # Don't hit API if already authenticated
        if self.authenticated:
            self.logger.debug(
                "Tried to authenticate previously authenticated backend")
            return

        try:
            self.client.users.ping()
            self.authenticated = True
        except mandrill.InvalidKeyError:
            self.authenticated = False
            self.logger.error("Invalid mandrill API key", exc_info=True)

            raise

    def get_message(self, user):
        """ Get the message content for a welcome email to a user """
        message = settings.MESSAGE_CONFIG
        message.update({
            'to': [
                {
                    'email': user.email,
                    'name': str(user),
                },
            ],
        })

        return message

    def send_email(self, user):
        """ Send greeting email to user """
        if not self.authenticated:
            self.authenticate()

        template_name = settings.TEMPLATE_NAME
        template_content = []
        message = self.get_message(user)

        return self.client.messages.send_template(
            template_name=template_name, template_content=template_content,
            message=message)
