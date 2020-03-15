import os
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "levechad.settings")
django.setup()

# your imports, e.g. Django models
from client.models import City, Language

# Language.objects.all().delete()
# City.objects.all().delete()

# From now onwards start your script..
if Language.objects.filter(name="עברית").first() == None:
    Language(name="עברית").save()
    Language(name="אנגלית").save()
    Language(name="רוסית").save()
    Language(name="צרפתית").save()
    Language(name="ערבית").save()
    Language(name="אחר").save()

with open('cities.json', encoding="utf8") as json_file:
    data = json.load(json_file)
    cities = list()
    for p in data:
        cities.append(City(name=p['name'], x=p['x'], y=p['y']))

    City.objects.bulk_create(cities)
