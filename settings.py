ADDRESS_HTML = """
<address>
  <strong>Know Me, LLC</strong> <br />
  710 Market Street Suite 42 <br />
  Chapel Hill, NC 27516 <br />
</address>
"""

API_KEY = 'secret key'

TEMPLATE_NAME = 'welcome-to-know-me'


# Import local settings if they exist
try:
    from local_settings import *        # noqa
except ImportError:
    pass
