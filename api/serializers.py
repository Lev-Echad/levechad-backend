from client.models import Volunteer, ParentalConsent, City, Language
from rest_framework import serializers
from client.validators import parental_consent_validator


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


class VolunteerSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display')
    moving_way = serializers.CharField(source='get_moving_way_display')
    wanted_assignments = serializers.ListField(source='get_wanted_assignments_list')

    class Meta:
        model = Volunteer
        fields = ['id', 'first_name', 'last_name', 'tz_number', 'phone_number', 'date_of_birth', 'age',
                  'gender', 'city', 'address', 'areas', 'organization', 'moving_way',
                  'week_assignments_capacity', 'wanted_assignments', 'email', 'email_verified', 'score',
                  'created_date', 'times_volunteered', 'languages']
