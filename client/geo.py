import re
import time

import geopy.geocoders
from django.conf import settings

# Used to convert city names with added information from MOI to proper city names readable by geocoders.
CITY_CLEANUP_RE = re.compile(r"^(.*?)(?: \(.*\))?$")


def run_query(address, coder=None, cache_dict=None, sleep=False):
    if coder is None:
        coder = get_geocoder()
    if cache_dict is not None and address in cache_dict:
        return cache_dict[address]
    # Required by some terms of service.
    if sleep:
        time.sleep(1)
    return coder.geocode(address)


def get_coordinates(city_name, address, cache_dict=None):
    """
    Returns the coordinates of the given address & city. Retreats to city coordinates if address fails. If geocoding
    city fails, raises LookupError.
    :rtype: geopy.location.Location
    """
    city_name = CITY_CLEANUP_RE.match(city_name).group(1)
    coder = get_geocoder()
    built_address = "%s, %s, ישראל" % (address, city_name)
    location = run_query(built_address, coder=coder, cache_dict=cache_dict)
    # If coding fails, attempt to resolve location by city.
    if not location:
        built_address = "%s, ישראל" % city_name
        location = run_query(
            built_address,
            coder=coder,
            cache_dict=cache_dict,
            sleep=(settings.LOCATOR == settings.LOCATOR.NOMINATIM)
        )

        if not location:
            raise LookupError("Failed to convert address to coordinates.")
    if cache_dict is not None:
        cache_dict[built_address] = location
    return location


def __bulk_geocode(addresses_list: list) -> dict:
    """
    WARNING: This function is UNTESTED. USE AT YOUR OWN RISK.
    :param addresses_list: List of tumples in the structure (city_name, address).
    :type addresses_list: list(tuple(city_name, address))
    :returns: A dict of Location objects corresponding to input addresses.
    """
    results_dict = {}
    cache_dict = {}
    for address_tuple in addresses_list:
        results_dict[address_tuple] = get_coordinates(address_tuple[0], address_tuple[1], cache_dict=cache_dict)
        if settings.LOCATOR == settings.LOCATOR.NOMINATIM:
            time.sleep(1)
    return results_dict


def get_geocoder():
    coder = None
    if settings.LOCATOR == settings.LOCATOR.NOMINATIM:
        # User agent required by Nominatim terms of use.
        coder = geopy.geocoders.Nominatim(user_agent="LevEchad geographic subsystem (beta)")
    elif settings.LOCATOR == settings.LOCATOR.GOOGLE:
        coder = geopy.geocoders.GoogleV3(api_key=settings.GOOGLE_API_SECRET_KEY)
    elif settings.LOCATOR == settings.LOCATOR.ARCGIS:
        raise NotImplementedError()
    return coder
