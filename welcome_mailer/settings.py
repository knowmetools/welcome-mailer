
API_KEY = 'secret key'

LOGGING_CONFIG = {
    'version': 1,

    'formatters': {
        'simple': {
            'format': '%(name)s - %(levelname)s - %(message)s',
        },
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'INFO',
            'stream': 'ext://sys.stdout',
        },
    },

    'root': {
        'handlers': [
            'console',
        ],
        'level': 'INFO',
    },
}

# Email Settings:
#
# These settings are used to generate a templated welcome email

# Shown at the bottom of our emails
ADDRESS_HTML = """
<address>
  <strong>Know Me, LLC</strong> <br />
  710 Market Street Suite 42 <br />
  Chapel Hill, NC 27516
</address>
"""

# Configuration dict for the message. For all options, see:
# https://mandrillapp.com/api/docs/messages.html#method=send-template

MESSAGE_CONFIG = {
    'subject': 'Welcome to Know Me',
    'from_email': 'no-reply@knowmetools.com',
    'from_name': 'Know Me Team',
    'track_opens': True,
    'track_clicks': True,
    'merge_language': 'mailchimp',
    'global_merge_vars': [
        {
            'name': 'COMPANY',
            'content': 'Know Me, LLC',
        },
        {
            'name': 'LIST_ADDRESS_HTML',
            'content': ADDRESS_HTML,
        },
    ],
}

# The name of the template used by mandrill

TEMPLATE_NAME = 'welcome-to-know-me'


# Import local settings if they exist
try:
    from welcome_mailer.local_settings import *        # noqa
except ImportError:
    pass
