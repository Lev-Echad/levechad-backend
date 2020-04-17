from django.db.models import Count
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken

import django_filters as filters

from client.models import Volunteer, HelpRequest, City, Area, Language
from client.validators import PHONE_NUMBER_REGEX
from api.serializers import VolunteerSerializer, RegistrationSerializer, HelpRequestSerializer, ShortCitySerializer, \
                            CreateHelpRequestSerializer, AreaSerializer, LanguageSerializer

import api.throttling


class CustomAuthToken(ObtainAuthToken):
    throttle_classes = [api.throttling.LoginThrottle]


# === Non-restricted API endpoints ===

class SendVerificationCodeViewSet(viewsets.ViewSet):
    throttle_classes = [api.throttling.SendSMSThrottle]

    def create(self, request):
        def _is_valid_phone_number(string):
            return PHONE_NUMBER_REGEX.search(string) is not None

        if request.data is None or len(request.data) == 0:
            return Response({'success': False, 'message': 'No data specified.'}, status=status.HTTP_400_BAD_REQUEST)

        if 'phoneNumber' not in request.data:
            return Response(
                {'success': False, 'message': 'The "phoneNumber" parameter must be specified.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = request.data['phoneNumber']
        if not _is_valid_phone_number(phone_number):
            return Response(
                {'success': False, 'message': 'Invalid phone number specified.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # TODO STUB - Implement in #198 - we might want to remove success and use status codes to indicate errors
        return Response({'success': True})


class CheckVerificationCodeViewSet(viewsets.ViewSet):
    throttle_classes = [api.throttling.CheckSMSThrottle]

    def create(self, request):
        if request.data is None or len(request.data) == 0:
            return Response({'success': False, 'message': 'No data specified.'}, status=status.HTTP_400_BAD_REQUEST)

        if 'phoneNumber' not in request.data or 'codeReceived' not in request.data:
            return Response(
                {'success': False, 'message': 'The "phoneNumber", "codeReceived" parameters must be specified.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = request.data['phoneNumber']
        code_received = request.data['codeReceived']

        # TODO STUB - Implement in #198 - we might want to remove success and use status codes to indicate errors
        return Response({'success': True, 'message': '', 'verified': True})


class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = RegistrationSerializer
    throttle_classes = [api.throttling.RegistrationThrottle]


class CreateHelpRequestViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = HelpRequest.objects.all()
    serializer_class = CreateHelpRequestSerializer
    throttle_classes = [api.throttling.RegistrationThrottle]


# === Authentication required API endpoints ===

class VolunteerFilter(filters.FilterSet):
    time_volunteered = filters.NumberFilter(lookup_expr='exact')
    time_volunteered__gt = filters.NumberFilter(method='time_volunteered_gt')
    time_volunteered__lt = filters.NumberFilter(method='time_volunteered_lt')

    def time_volunteered_gt(self, queryset, field_name, value):
        return queryset.filter(time_volunteered__gt=value)

    def time_volunteered_lt(self, queryset, field_name, value):
        return queryset.filter(time_volunteered__lt=value)

    class Meta:
        model = Volunteer
        fields = {
            'id': ['exact'],
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'tz_number': ['exact', 'icontains'],
            'phone_number': ['exact', 'icontains'],
            'date_of_birth': ['gt', 'lt', 'exact'],
            'age': ['gt', 'lt', 'exact'],
            'gender': ['exact'],
            'city': ['exact', 'in'],
            'neighborhood': ['exact', 'icontains'],
            'areas': ['exact'],
            'moving_way': ['exact'],
            'week_assignments_capacity': ['exact', 'range'],
            'wanted_assignments': ['exact'],
            'score': ['exact'],
            'created_date': ['gt', 'lt', 'exact'],
            'organization': ['exact', 'in']
        }


class HelpRequestsFilter(filters.FilterSet):
    class Meta:
        model = HelpRequest
        fields = {
            'id': ['exact'],
            'city': ['exact', 'in'],
            'area': ['exact', 'in'],
            'status': ['exact', 'in'],
            'type': ['exact', 'in']
        }


class VolunteersViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Volunteer.objects.all().order_by('-created_date').annotate(time_volunteered=Count('helprequest'))
    serializer_class = VolunteerSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = VolunteerFilter
    throttle_classes = [api.throttling.HamalDataListThrottle]


class HelpRequestsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = HelpRequest.objects.all().order_by('-created_date')
    serializer_class = HelpRequestSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = HelpRequestsFilter
    throttle_classes = [api.throttling.HamalDataListThrottle]


class ListByNameViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = None

    def list(self, request):
        try:
            response = super().list(request)
            response.data = [item['name'] for item in response.data]
            return response
        except ValidationError as err:
            return Response(
                {'detail': err.detail},
                status=status.HTTP_400_BAD_REQUEST
            )


class CityAutocompleteViewSet(ListByNameViewSet):
    MINIMUM_FILTER_LENGTH = 2
    STARTSWITH_QUERY_PARAMETER = 'name__startswith'

    serializer_class = ShortCitySerializer
    throttle_classes = [api.throttling.CityAutocompleteThrottle]

    def get_queryset(self):
        """
        Requires the "startswith" parameter to exist & not be below MINIMUM_FILTER_LENGTH
        """
        startswith = self.request.query_params.get(type(self).STARTSWITH_QUERY_PARAMETER, None)
        if startswith is None or len(startswith) < type(self).MINIMUM_FILTER_LENGTH:
            raise ValidationError(''.join([
                f'{type(self).STARTSWITH_QUERY_PARAMETER} parameter must be ',
                f'above {type(self).MINIMUM_FILTER_LENGTH} characters.'
            ]))

        return City.objects.all().filter(name__startswith=startswith).order_by('name')


class AreasViewSet(ListByNameViewSet):
    queryset = Area.objects.all().order_by('name')
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [api.throttling.UserChoicesListThrottle]


class LanguagesViewSet(ListByNameViewSet):
    queryset = Language.objects.all().order_by('name')
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [api.throttling.UserChoicesListThrottle]
