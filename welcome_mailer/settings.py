ADDRESS_HTML = """
<address>
  <strong>Know Me, LLC</strong> <br />
  710 Market Street Suite 42 <br />
  Chapel Hill, NC 27516 <br />
</address>
"""

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

TEMPLATE_NAME = 'welcome-to-know-me'


# Import local settings if they exist
try:
    from welcome_mailer.local_settings import *        # noqa
except ImportError:
    pass
