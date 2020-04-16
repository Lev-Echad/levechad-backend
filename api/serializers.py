from rest_framework import serializers
from client.validators import parental_consent_validator

from client.models import Volunteer, ParentalConsent, City, Language, HelpRequest, Area


class ParentalConsentSerializer(serializers.ModelSerializer):
    # Currently, nested serializer field required=False doesn't work.
    # Link to bug in DRF: https://github.com/encode/django-rest-framework/issues/2719
    # Declaring these fields as required=False is the workaround so ParentalConsent won't be required.
    parent_name = serializers.CharField(required=False)
    parent_id = serializers.CharField(required=False)

    class Meta:
        model = ParentalConsent
        fields = ['parent_name', 'parent_id']


class RegistrationSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    languages = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), many=True)
    wanted_assignments = serializers.MultipleChoiceField(choices=Volunteer.WANTED_ASSIGNMENTS)
    parental_consent = ParentalConsentSerializer()

    class Meta:
        model = Volunteer
        fields = ['first_name', 'last_name', 'tz_number', 'date_of_birth', 'gender', 'city', 'address', 'moving_way',
                  'week_assignments_capacity', 'wanted_assignments', 'phone_number', 'email', 'parental_consent',
                  'languages']

    def validate(self, data):
        parental_consent_validator(data)

        return data

    def create(self, validated_data):
        parental_consent_data = validated_data.pop('parental_consent')
        languages = [Language.objects.get(name=name) for name in validated_data.pop('languages')]
        volunteer = Volunteer.objects.create(**validated_data)

        volunteer.languages.set(languages)
        ParentalConsent.objects.create(volunteer=volunteer, **parental_consent_data)
        return volunteer


class CitySerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())

    class Meta:
        model = City
        fields = ['name', 'x', 'y', 'region']


class ShortCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']


class VolunteerSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display')
    moving_way = serializers.CharField(source='get_moving_way_display')
    wanted_assignments = serializers.ListField(source='get_wanted_assignments_list')
    city = CitySerializer()

    class Meta:
        model = Volunteer
        fields = ['id', 'first_name', 'last_name', 'tz_number', 'phone_number', 'date_of_birth', 'age',
                  'gender', 'city', 'address', 'areas', 'organization', 'moving_way',
                  'week_assignments_capacity', 'wanted_assignments', 'email', 'email_verified', 'score',
                  'created_date', 'times_volunteered', 'languages']


class ShortVolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ['id', 'full_name']


class HelpRequestSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    type = serializers.CharField(source='get_type_display')
    request_reason = serializers.CharField(source='get_request_reason_display')
    status = serializers.CharField(source='get_status_display')
    helping_volunteer = ShortVolunteerSerializer()

    class Meta:
        model = HelpRequest
        fields = ['id', 'full_name', 'phone_number', 'area', 'city', 'address', 'notes', 'type', 'type_text',
                  'request_reason', 'status', 'status_updater', 'helping_volunteer', 'created_date']
