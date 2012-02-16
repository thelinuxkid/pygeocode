import fudge

from nose.tools import eq_ as eq
from cStringIO import StringIO
from collections import OrderedDict

from pygeocode import geocoder
from pygeocode.test.util import assert_raises

class TestGeocoder(object):
    def setUp(self):
        fudge.clear_expectations()

    @fudge.with_fakes
    def test_yahoo_geocode_simple(self):
        fake_urllib2 = fudge.Fake('urllib2')
        fake_urllib2.remember_order()

        urlopen = fake_urllib2.expects('urlopen')
        urlopen.with_args(
            'http://where.yahooapis.com/geocode?'
            'location=1821+Pacific+Coast+Hwy%2C+Hermosa+Beach%2C+California+90254'
            '&flags=J&appid=foo'
            )
        res = """{"ResultSet":{"version":"1.0","Error":0,"ErrorMessage":"No error","Locale":"us_US","Quality":87,"Found":1,"Results":[{"quality":87,"latitude":"33.86829","longitude":"-118.394024","offsetlat":"33.868267","offsetlon":"-118.394174","radius":500,"name":"","line1":"1821 Pacific Coast Hwy, #11","line2":"Hermosa Beach, CA  90254-3125","line3":"","line4":"United States","house":"1821","street":"Pacific Coast Hwy","xstreet":"","unittype":"","unit":"#11","postal":"90254-3125","neighborhood":"","city":"Hermosa Beach","county":"Los Angeles County","state":"California","country":"United States","countrycode":"US","statecode":"CA","countycode":"","uzip":"90254","hash":"0F843448232C6E64","woeid":12795734,"woetype":11}]}}"""
        urlopen.returns(StringIO(res))

        data = geocoder.geocode_yahoo(
            '1821 Pacific Coast Hwy, Hermosa Beach, California 90254',
            'foo',
            _urllib2=fake_urllib2,
            )

        expected = OrderedDict([
            ('lat', 33.868290),
            ('lng', -118.394024),
            ])
        eq(data, expected)

    @fudge.with_fakes
    def test_yahoo_geocode_no_app_id(self):
        fake_urllib2 = fudge.Fake('urllib2')
        fake_urllib2.remember_order()

        urlopen = fake_urllib2.expects('urlopen')
        urlopen.with_args(
            'http://where.yahooapis.com/geocode?'
            'location=1821+Pacific+Coast+Hwy%2C+Hermosa+Beach%2C+California+90254'
            '&flags=J'
            )
        res = """{"ResultSet":{"version":"1.0","Error":0,"ErrorMessage":"No error","Locale":"us_US","Quality":87,"Found":1,"Results":[{"quality":87,"latitude":"33.86829","longitude":"-118.394024","offsetlat":"33.868267","offsetlon":"-118.394174","radius":500,"name":"","line1":"1821 Pacific Coast Hwy, #11","line2":"Hermosa Beach, CA  90254-3125","line3":"","line4":"United States","house":"1821","street":"Pacific Coast Hwy","xstreet":"","unittype":"","unit":"#11","postal":"90254-3125","neighborhood":"","city":"Hermosa Beach","county":"Los Angeles County","state":"California","country":"United States","countrycode":"US","statecode":"CA","countycode":"","uzip":"90254","hash":"0F843448232C6E64","woeid":12795734,"woetype":11}]}}"""
        urlopen.returns(StringIO(res))

        data = geocoder.geocode_yahoo(
            '1821 Pacific Coast Hwy, Hermosa Beach, California 90254',
            _urllib2=fake_urllib2,
            )

        expected = OrderedDict([
            ('lat', 33.868290),
            ('lng', -118.394024),
            ])
        eq(data, expected)

    @fudge.with_fakes
    def test_yahoo_geocode_ambiguous_result_error(self):
        fake_urllib2 = fudge.Fake('urllib2')
        fake_urllib2.remember_order()

        urlopen = fake_urllib2.expects('urlopen')
        urlopen.with_args(
            'http://where.yahooapis.com/geocode?'
            'location=1821+Pacific+Coast+Hwy%2C+Hermosa+Beach%2C+California+90254'
            '&flags=J&appid=foo'
            )
        res = """{"ResultSet":{"version":"1.0","Error":0,"ErrorMessage":"No error","Locale":"us_US","Quality":87,"Found":2,"Results":[{"quality":87,"latitude":"33.86829","longitude":"-118.394024","offsetlat":"33.868267","offsetlon":"-118.394174","radius":500,"name":"","line1":"1821 Pacific Coast Hwy, #11","line2":"Hermosa Beach, CA  90254-3125","line3":"","line4":"United States","house":"1821","street":"Pacific Coast Hwy","xstreet":"","unittype":"","unit":"#11","postal":"90254-3125","neighborhood":"","city":"Hermosa Beach","county":"Los Angeles County","state":"California","country":"United States","countrycode":"US","statecode":"CA","countycode":"","uzip":"90254","hash":"0F843448232C6E64","woeid":12795734,"woetype":11},{"quality":87,"latitude":"33.86829","longitude":"-118.394024","offsetlat":"33.868267","offsetlon":"-118.394174","radius":500,"name":"","line1":"1821 Pacific Coast Hwy, #11","line2":"Hermosa Beach, CA  90254-3125","line3":"","line4":"United States","house":"1821","street":"Pacific Coast Hwy","xstreet":"","unittype":"","unit":"#11","postal":"90254-3125","neighborhood":"","city":"Hermosa Beach","county":"Los Angeles County","state":"California","country":"United States","countrycode":"US","statecode":"CA","countycode":"","uzip":"90254","hash":"0F843448232C6E64","woeid":12795734,"woetype":11}]}}"""
        urlopen.returns(StringIO(res))

        msg = assert_raises(
            geocoder.GeocoderAmbiguousResultError,
            geocoder.geocode_yahoo,
            '1821 Pacific Coast Hwy, Hermosa Beach, California 90254',
            'foo',
            _urllib2=fake_urllib2,
            )

        expected = ('Got more than one result for the requested address: '
                    + '1821 Pacific Coast Hwy, Hermosa Beach, California 90254'
                    )
        eq(str(msg), expected)

    @fudge.with_fakes
    def test_yahoo_geocode_status_error(self):
        fake_urllib2 = fudge.Fake('urllib2')
        fake_urllib2.remember_order()

        urlopen = fake_urllib2.expects('urlopen')
        urlopen.with_args(
            'http://where.yahooapis.com/geocode?'
            'location=1821+Pacific+Coast+Hwy%2C+Hermosa+Beach%2C+California+90254'
            '&flags=J&appid=foo'
            )
        res = """{"ResultSet":{"version":"1.0","Error":1,"ErrorMessage":"Feature not supported","Locale":"us_US","Quality":87,"Found":0,"Results":[]}}"""
        urlopen.returns(StringIO(res))

        msg = assert_raises(
            geocoder.GeocoderStatusError,
            geocoder.geocode_yahoo,
            '1821 Pacific Coast Hwy, Hermosa Beach, California 90254',
            'foo',
            _urllib2=fake_urllib2,
            )

        expected = 'The API call failed with status code: 1'
        eq(str(msg), expected)

    @fudge.with_fakes
    def test_yahoo_geocode_zero_result(self):
        fake_urllib2 = fudge.Fake('urllib2')
        fake_urllib2.remember_order()

        urlopen = fake_urllib2.expects('urlopen')
        urlopen.with_args(
            'http://where.yahooapis.com/geocode?'
            'location=1821+Pacific+Coast+Hwy%2C+Hermosa+Beach%2C+California+90254'
            '&flags=J&appid=foo'
            )
        res = """{"ResultSet":{"version":"1.0","Error":0,"ErrorMessage":"No error","Locale":"us_US","Quality":0,"Found":0}}"""
        urlopen.returns(StringIO(res))

        data = geocoder.geocode_yahoo(
            '1821 Pacific Coast Hwy, Hermosa Beach, California 90254',
            'foo',
            _urllib2=fake_urllib2,
            )
        eq(None, data)

    @fudge.with_fakes
    def test_google_geocode_simple(self):
        fake_urllib2 = fudge.Fake('urllib2')
        fake_urllib2.remember_order()

        urlopen = fake_urllib2.expects('urlopen')
        urlopen.with_args(
            'http://maps.googleapis.com/maps/api/geocode/json?'
            'address=1600+Amphitheatre+Parkway%2C+Mountain+View%2C+CA'
            '&sensor=false'
            )
        res = """{"status": "OK", "results": [{"geometry": {"location": {"lat": 37.421972, "lng": -122.084143}, "viewport": {"northeast": {"lat": 37.4251196, "lng": -122.0809954}, "southwest": {"lat": 37.4188244, "lng": -122.0872906}}, "location_type": "ROOFTOP"}, "address_components": [{"long_name": "1600", "types": ["street_number"], "short_name": "1600"}, {"long_name": "Amphitheatre Pkwy", "types": ["route"], "short_name": "Amphitheatre Pkwy"}, {"long_name": "Mountain View", "types": ["locality", "political"], "short_name": "Mountain View"}, {"long_name": "California", "types": ["administrative_area_level_1", "political"], "short_name": "CA"}, {"long_name": "United States", "types": ["country", "political"], "short_name": "US"}, {"long_name": "94043", "types": ["postal_code"], "short_name": "94043"}], "formatted_address": "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA", "types": ["street_address"]}]}"""
        urlopen.returns(StringIO(res))

        data = geocoder.geocode_google(
            '1600 Amphitheatre Parkway, Mountain View, CA',
            _urllib2=fake_urllib2,
            )

        expected = OrderedDict([
            ('lat', 37.4219720),
            ('lng', -122.0841430),
            ])
        eq(data, expected)

    @fudge.with_fakes
    def test_google_geocode_ambiguous_result_error(self):
        fake_urllib2 = fudge.Fake('urllib2')
        fake_urllib2.remember_order()

        urlopen = fake_urllib2.expects('urlopen')
        urlopen.with_args(
            'http://maps.googleapis.com/maps/api/geocode/json?'
            'address=double+foo%2C+CA'
            '&sensor=false'
            )
        res = """{"status": "OK", "results": ["foo", "bar"]}"""
        urlopen.returns(StringIO(res))

        msg = assert_raises(
            geocoder.GeocoderAmbiguousResultError,
            geocoder.geocode_google,
            'double foo, CA',
            _urllib2=fake_urllib2,
            )

        expected = ('Got more than one result for the requested address: '
                    + 'double foo, CA'
                    )
        eq(str(msg), expected)

    @fudge.with_fakes
    def test_google_geocode_status_error(self):
        fake_urllib2 = fudge.Fake('urllib2')
        fake_urllib2.remember_order()

        urlopen = fake_urllib2.expects('urlopen')
        urlopen.with_args(
            'http://maps.googleapis.com/maps/api/geocode/json?'
            'address=1600+Amphitheatre+Parkway%2C+Mountain+View%2C+CA'
            '&sensor=false'
            )
        res = """{"status": "INVALID_REQUEST", "results": []}"""
        urlopen.returns(StringIO(res))

        msg = assert_raises(
            geocoder.GeocoderStatusError,
            geocoder.geocode_google,
            '1600 Amphitheatre Parkway, Mountain View, CA',
            _urllib2=fake_urllib2,
            )

        expected = 'The API call failed with status code: INVALID_REQUEST'
        eq(str(msg), expected)

    @fudge.with_fakes
    def test_google_geocode_zero_result(self):
        fake_urllib2 = fudge.Fake('urllib2')
        fake_urllib2.remember_order()

        urlopen = fake_urllib2.expects('urlopen')
        urlopen.with_args(
            'http://maps.googleapis.com/maps/api/geocode/json?'
            'address=foo+bar'
            '&sensor=false'
            )
        res = """{"status": "ZERO_RESULTS", "results": []}"""
        urlopen.returns(StringIO(res))

        data = geocoder.geocode_google(
            'foo bar',
            _urllib2=fake_urllib2,
            )
        eq(None, data)

    @fudge.with_fakes
    def test_google_geocode_rate_limit_error(self):
        fake_urllib2 = fudge.Fake('urllib2')
        fake_urllib2.remember_order()

        urlopen = fake_urllib2.expects('urlopen')
        urlopen.with_args(
            'http://maps.googleapis.com/maps/api/geocode/json?'
            'address=1600+Amphitheatre+Parkway%2C+Mountain+View%2C+CA'
            '&sensor=false'
            )
        res = """{"status": "OVER_QUERY_LIMIT", "results": []}"""
        urlopen.returns(StringIO(res))

        msg = assert_raises(
            geocoder.GeocoderRateLimitError,
            geocoder.geocode_google,
            '1600 Amphitheatre Parkway, Mountain View, CA',
            _urllib2=fake_urllib2,
            )

        expected = 'The geocoder has exceeded its daily request limit'
        eq(str(msg), expected)
