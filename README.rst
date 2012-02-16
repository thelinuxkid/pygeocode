=========
Pygeocode
=========

Description
===========

        Pygeocode leverages multiple public geocoding APIs including
        Google's Geocoding API and Yahoo's Place Finder. Having several
        APIs available is specially useful when the user has reached one
        API's rate limit or when an API returns ambiguous results, or
        no results at all.

Examples
========

        Use Google's Geocoding API::

            from pygeocode import geocoder

            address = '1600 Amphitheatre Pkwy, Mountain View, CA'
            res = geocoder.geocode_google(address)
            print res['lat'], res['lng']

        Use Yahoo's Place Finder API::

            from pygeocode import geocoder

            app_id = <you_app_id>
            address = '1600 Amphitheatre Pkwy, Mountain View, CA'
            res = geocoder.geocode_yahoo(address, app_id)
            print res['lat'], res['lng']
