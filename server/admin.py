from django.contrib import admin

from client.models import Volunteer
from client.models import Language
from client.models import City
from client.models import VolunteerSchedule


admin.site.register(Volunteer)
admin.site.register(Language)
admin.site.register(City)
admin.site.register(VolunteerSchedule)
