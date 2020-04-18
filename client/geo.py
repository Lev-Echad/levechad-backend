import re
import time

import geopy.geocoders
from django.conf import settings

from client.models import Volunteer, HelpRequest


class Locators:
    NOMINATIM = 'NOMINATIM'
    GOOGLE = 'GOOGLE'
    ARCGIS = 3


ADDRESS_CLEANUP_RE = re.compile(r"^(.*?)(?: \(.*\))?$")


def get_coordinates(city_name, address):
    city_name = ADDRESS_CLEANUP_RE.match(city_name).group(1)
    coder = get_geocoder()
    built_address = "%s, %s, ישראל" % (address, city_name)
    location = coder.geocode(built_address)
    # If coding fails, attempt to resolve city_name.
    if not location:
        if settings.LOCATOR == Locators.NOMINATIM:
            time.sleep(1)
        built_address = "%s, ישראל" % city_name
        location = coder.geocode(built_address)

        if not location:
            raise LookupError("Failed to convert address to coordinates.")
    return location


def get_geocoder():
    coder = None
    if settings.LOCATOR == Locators.NOMINATIM:
        # User agent required by Nominatim terms of use.
        coder = geopy.geocoders.Nominatim(user_agent="LevEchad geographic subsystem (beta)")
    elif settings.LOCATOR == Locators.GOOGLE:
        coder = geopy.geocoders.GoogleV3(api_key=settings.GOOGLE_API_SECRET_KEY)
    elif settings.LOCATOR == Locators.ARCGIS:
        raise NotImplementedError()
    return coder


def add_volunteer_location(volunteer):
    pass
