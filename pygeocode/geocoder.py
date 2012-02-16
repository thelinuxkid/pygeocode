import urllib2
import urllib
import urlparse
import logging

from collections import OrderedDict
from pygeocode.util import read_json

log = logging.getLogger(__name__)

google_api_url = 'http://maps.googleapis.com/maps/api/geocode/json'
yahoo_places_api_url = 'http://where.yahooapis.com/geocode'

class GeocoderError(Exception):
    """There was a problem while geocoding"""
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return '%s: %s' % (self.__doc__, self._msg)

class GeocoderAmbiguousResultError(GeocoderError):
    """Got more than one result for the requested address"""
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return '%s: %s' % (self.__doc__, self._msg)

class GeocoderStatusError(GeocoderError):
    """The API call failed with status code"""
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return '%s: %s' % (self.__doc__, self.code)

class GeocoderRateLimitError(Exception):
    """The geocoder has exceeded its daily request limit"""
    def __init__(self):
        pass

    def __str__(self):
        return '%s' % (self.__doc__)

def _log_url(url):
    # Unquote query params safely
    debug_url = urlparse.urlparse(url)
    debug_url = urlparse.urlunparse(debug_url)
    log.debug(
        'Requesting url {url}'.format(
            url=debug_url,
            ),
        )

def geocode_google(
    address,
    _urllib2=None,
    ):
    if _urllib2 is None:
        _urllib2 = urllib2

    query = OrderedDict([
        ('address', address),
        ('sensor', 'false'),
        ])
    query = urllib.urlencode(query)
    url = '{api_url}?{query}'.format(
        api_url=google_api_url,
        query=query,
        )

    _log_url(url)

    res = _urllib2.urlopen(url)
    data = read_json(res)

    status = data.pop('status')
    if status == 'OVER_QUERY_LIMIT':
        raise GeocoderRateLimitError()
    if status == 'ZERO_RESULTS':
        return None
    if status != 'OK':
        raise GeocoderStatusError(status)

    results = data.pop('results')
    if len(results) != 1:
        raise GeocoderAmbiguousResultError(address)

    # We'll want to know if the API result fields change
    location = results[0]['geometry']['location']
    result = OrderedDict(
        lat=float(location['lat']),
        lng=float(location['lng']),
        )

    return result

def geocode_yahoo(
    address,
    appid=None,
    _urllib2=None,
    ):

    if _urllib2 is None:
        _urllib2 = urllib2

    query = OrderedDict([
        ('location', address),
        ('flags', 'J'),
        ])
    if appid is not None:
        query['appid'] = appid
    query = urllib.urlencode(query)
    url = '{api_url}?{query}'.format(
        api_url=yahoo_places_api_url,
        query=query,
        )

    _log_url(url)

    res = _urllib2.urlopen(url)
    data = read_json(res)

    data = data.pop('ResultSet')

    error_code = data.pop('Error')
    error_code = int(error_code)
    if error_code > 0:
        raise GeocoderStatusError(error_code)

    results = data.pop('Results', None)
    if not results:
        return None
    if len(results) > 1:
        raise GeocoderAmbiguousResultError(address)

    # We'll want to know if the API result fields change
    result = OrderedDict(
        lat=float(results[0]['latitude']),
        lng=float(results[0]['longitude']),
        )

    return result
