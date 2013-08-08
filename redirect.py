import urlparse

from google.appengine.ext.webapp import RequestHandler

from config import config
import custom_exceptions
import os
from .gae_bingo import bingo, _iri_to_uri

class Redirect(RequestHandler):
    def get(self):
        """ Score conversions and redirect as specified by url params

        Expects a 'continue' url parameter for the destination,
        and a 'conversion_name' url parameter for each conversion to score.
        """
        cont = self.request.get('continue', default_value='/')

        # Check whether redirecting to an absolute or relative url
        netloc = urlparse.urlsplit(cont).netloc
        if (netloc and
                netloc != os.environ["HTTP_HOST"] and
                not config.is_safe_hostname(netloc)):
            # Disallow open redirects to other domains.
            raise custom_exceptions.InvalidRedirectURLError(
                    "Redirecting to an absolute url is not allowed.")

        conversion_names = self.request.get_all('conversion_name')

        if len(conversion_names):
            bingo(conversion_names)

        self.redirect(_iri_to_uri(cont))
