from django.contrib import admin

from client.models import Volunteer
from client.models import Language
from client.models import City
from client.models import Area
from client.models import HamalUser
from client.models import VolunteerSchedule
from client.models import HelpRequest


admin.site.register(Volunteer)
admin.site.register(Language)
admin.site.register(City)
admin.site.register(VolunteerSchedule)
admin.site.register(HelpRequest)
admin.site.register(HamalUser)
admin.site.register(Area)
