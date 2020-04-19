from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from client.validators import parental_consent_validator, minimum_age_validator, phone_number_validator, \
    unique_id_number_validator, id_number_validator
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
    date_of_birth = serializers.DateField(required=True)
    gender = serializers.ChoiceField(required=True, choices=Volunteer.GENDERS)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    languages = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), many=True, required=True)
    wanted_assignments = serializers.MultipleChoiceField(choices=Volunteer.WANTED_ASSIGNMENTS)
    email = serializers.EmailField(required=True)
    parental_consent = ParentalConsentSerializer()

    class Meta:
        model = Volunteer
        fields = ['first_name', 'last_name', 'tz_number', 'date_of_birth', 'gender', 'city', 'address', 'moving_way',
                  'week_assignments_capacity', 'wanted_assignments', 'phone_number', 'email', 'parental_consent',
                  'languages']

    def validate_date_of_birth(self, date_of_birth):
        minimum_age_validator(date_of_birth)
        return date_of_birth

    def validate_phone_number(self, phone_number):
        phone_number_validator(phone_number)
        return phone_number

    def validate_tz_number(self, tz_number):
        id_number_validator(tz_number)
        unique_id_number_validator(tz_number)
        return tz_number

    def validate_languages(self, languages):
        if not languages:
            raise ValidationError('No languages specified.')
        return languages

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
        fields = ['name', 'region']


class ShortCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']


class VolunteerSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display')
    moving_way = serializers.CharField(source='get_moving_way_display')
    wanted_assignments = serializers.ListField(source='get_wanted_assignments_list')
    city = CitySerializer()
    num_helprequests = serializers.IntegerField()  # annotated in queryset

    class Meta:
        model = Volunteer
        fields = ['id', 'first_name', 'last_name', 'tz_number', 'phone_number', 'date_of_birth', 'age',
                  'gender', 'city', 'address', 'organization', 'moving_way', 'week_assignments_capacity',
                  'wanted_assignments', 'email', 'email_verified', 'score', 'created_date', 'num_helprequests',
                  'languages', 'location_latitude', 'location_longitude']


class ShortVolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ['id', 'full_name']


class MatchingVolunteerSerializer(serializers.ModelSerializer):
    moving_way = serializers.CharField(source='get_moving_way_display')

    class Meta:
        model = Volunteer
        fields = ['id', 'full_name', 'city', 'address', 'phone_number', 'email', 'location_latitude',
                  'location_longitude', 'moving_way']


class MapHelpRequestSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = HelpRequest
        fields = ['id', 'full_name', 'location_latitude', 'location_longitude', 'status', 'helping_volunteer']


class CreateHelpRequestSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = HelpRequest
        fields = ['full_name', 'phone_number', 'city', 'address', 'notes', 'type', 'type_text', 'request_reason']

    def validate_phone_number(self, phone_number):
        phone_number_validator(phone_number)
        return phone_number


class HelpRequestSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    type = serializers.CharField(source='get_type_display')
    request_reason = serializers.CharField(source='get_request_reason_display')
    status = serializers.CharField(source='get_status_display')
    helping_volunteer = ShortVolunteerSerializer()

    class Meta:
        model = HelpRequest
        fields = ['id', 'full_name', 'phone_number', 'city', 'address', 'notes', 'type', 'type_text',
                  'request_reason', 'status', 'status_updater', 'helping_volunteer', 'created_date']


class UpdateHelpRequestSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = HelpRequest
        fields = ['notes', 'helping_volunteer', 'status', 'type_text']


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['name']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['name']
