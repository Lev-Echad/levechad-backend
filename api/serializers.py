from client.models import Volunteer, VolunteerSchedule, City
from rest_framework import serializers


class RegistrationSerializer(serializers.HyperlinkedModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Volunteer
        fields = ['first_name', 'last_name', 'tz_number', 'date_of_birth', 'gender', 'city', 'address', 'moving_way',
                  'week_assignments_capacity', 'wanted_assignments', 'phone_number', 'email']


class VolunteerSerializer(serializers.HyperlinkedModelSerializer):
    city = serializers.CharField(source='city.name')
    areas = serializers.CharField(source='get_area_names')
    languages = serializers.CharField(source='get_language_names')
    gender = serializers.CharField(source='get_gender_display')
    moving_way = serializers.CharField(source='get_moving_way_display')
    wanted_assignments = serializers.CharField(source='get_wanted_assignments_display')

    class Meta:
        model = Volunteer
        fields = ['id', 'first_name', 'last_name', 'tz_number', 'phone_number', 'date_of_birth', 'age',
                  'gender', 'city', 'address', 'areas', 'organization', 'moving_way',
                  'week_assignments_capacity', 'wanted_assignments', 'email', 'email_verified', 'score',
                  'created_date', 'times_volunteered', 'languages']
