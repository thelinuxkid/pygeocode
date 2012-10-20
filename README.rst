=========
pygeocode
=========

Description
===========

pygeocode leverages multiple public geocoding APIs including
Google's Geocoding API and Yahoo's Place Finder. Having several
APIs available is specially useful when the user has reached one
API's rate limit or when an API returns ambiguous results, or
no results at all.

Installation
============

Install using pip::

    pip install pyusps

or easy_install::

    easy_install pyusps

Examples
========

Using Google's Geocoding API::

    from pygeocode import geocoder

    address = '1600 Amphitheatre Pkwy, Mountain View, CA'
    res = geocoder.geocode_google(address)
    print res['lat'], res['lng']


Using Yahoo's Place Finder API::

    from pygeocode import geocoder

    app_id = <you_app_id>
    address = '1600 Amphitheatre Pkwy, Mountain View, CA'
    res = geocoder.geocode_yahoo(address, app_id)
    print res['lat'], res['lng']


Full example::

    import optparse
    import functools
    import logging

    from pygeocode import geocoder

    log = logging.getLogger(__name__)

    def main(address, appid=None):
        yahoo_geocoder = functools.partial(
            geocoder.geocode_yahoo,
            appid=appid,
            )
        geocoders = [yahoo_geocoder, geocoder.geocode_google]
        for geocoder_ in geocoders:
            try:
                res = geocoder_(address)
            except geocoder.GeocoderError, e:
                log.error(str(e))
            else:
                return res

    if __name__ == '__main__':
        parser = optparse.OptionParser(
            usage='%prog ADDRESS [OPTS]',
            )
        parser.add_option(
            '--yahoo-appid',
            help='The Yahoo Application ID to be used in the API call',
            )
        parser.add_option(
            '-v', '--verbose',
            help='Verbose mode [default %default]',
            action="store_true", dest="verbose"
            )
        parser.set_defaults(
            verbose=False,
            )

        options, args = parser.parse_args()
        try:
            (address,) = args
        except ValueError:
            parser.error('Wrong number of arguments.')

        logging.basicConfig(
            level=logging.DEBUG if options.verbose else logging.INFO,
            format='%(asctime)s.%(msecs)03d %(name)s: %(levelname)s: %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S',
            )

        res = main(address, appid=options.yahoo_appid)

        if res:
            out = '"{address}" is at coordinates {lat},{lng}'.format(
                address=address,
                lat=res['lat'],
                lng=res['lng'],
                )
        else:
            out = 'No results found for "{address}"'.format(
                address=address,
                )

        print out

Developing
==========

External dependencies
---------------------

    - python-dev
    - python-setuptools
    - python-virtualenv

Setup
-----

To start developing run the following commands from the project's base
directory. You can download the source from
https://github.com/thelinuxkid/pygeocode::

    # I like to install the virtual environment in its own
    # hidden repo but you don't have to
    virtualenv .virtual
    # I leave the magic to Ruby developers (.virtual/bin/activate)
    # but you don't have to agree with me
    .virtual/bin/python setup.py develop
    # Install the testing dependecies. Pip doesn't seem to handle
    # extras_require yet: https://github.com/pypa/pip/issues/7.
    # So, use easy_install.
    # At this point, pygeocode will already be in easy-install.pth.
    # So easy_install will not attempt to download it
    .virtual/bin/easy_install pygeocode[test]

If you like to use ipython you can install it with the dev
requirement::

    .virtual/bin/easy_install pygeocode[dev]

Testing
-------

To run the unit-tests run the following command from the project's
base directory::

    .virtual/bin/nosetests
