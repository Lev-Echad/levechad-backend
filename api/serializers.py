from client.models import Volunteer, VolunteerSchedule, City
from rest_framework import serializers


class RegistrationSerializer(serializers.HyperlinkedModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Volunteer
        fields = ['first_name', 'last_name', 'tz_number', 'date_of_birth', 'sex', 'city', 'address', 'moving_way',
                  'week_assignments_capacity', 'wanted_assignments']


class VolunteerSerializer(serializers.HyperlinkedModelSerializer):
    city = serializers.CharField(source='city.name')
    areas = serializers.CharField(source='get_area_names')
    languages = serializers.CharField(source='get_language_names')
    schedule = serializers.PrimaryKeyRelatedField(queryset=VolunteerSchedule.objects.all())

    class Meta:
        model = Volunteer
        fields = '__all__'
