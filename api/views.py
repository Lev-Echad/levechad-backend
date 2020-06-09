from datetime import datetime

from django.http import HttpResponse

from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action

from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from levechad import settings

from client.models import Volunteer, HelpRequest, City, Area, Language
from client.validators import PHONE_NUMBER_REGEX
from api.serializers import VolunteerSerializer, RegistrationSerializer, HelpRequestSerializer, ShortCitySerializer, \
    CreateHelpRequestSerializer, AreaSerializer, LanguageSerializer, \
    MatchingVolunteerSerializer, MapHelpRequestSerializer, UpdateHelpRequestSerializer, VolunteerFreezeSerializer, \
    UpdateVolunteerSerializer

from server.resources import VolunteerResource, HelpRequestResource

import api.throttling
import api.filters


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
    serializer_class = RegistrationSerializer
    throttle_classes = [api.throttling.RegistrationThrottle]


class CreateHelpRequestViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CreateHelpRequestSerializer
    throttle_classes = [api.throttling.RegistrationThrottle]


# === Authentication required API endpoints ===


class VolunteersViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Volunteer.objects.all_with_helprequests_count().order_by('-created_date')
    serializer_class = VolunteerSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = api.filters.VolunteerFilter
    throttle_classes = [api.throttling.HamalDataListThrottle]

    BEST_MATCH_VOLUNTEERS_LIMIT = 20

    @action(detail=False, methods=['get'], url_path='best_match')
    def best_matches_for_helprequest(self, request):
        """
        Returns the BEST_MATCH_VOLUNTEERS_LIMIT best matched volunteers for the given help request.
        """
        helprequest_id = request.query_params.get('helprequest_id', None)
        if helprequest_id is None:
            return Response(
                {'helprequest_id': 'This field must be specified.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            helprequest_id = int(helprequest_id)
            helprequest = HelpRequest.objects.get(pk=helprequest_id)
        except (ValueError, HelpRequest.DoesNotExist):
            return Response(
                {'helprequest_id': f'No help request with ID {helprequest_id} found.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        coords = (helprequest.location_latitude, helprequest.location_longitude)
        queryset = Volunteer.objects.all_by_score(coords)[:self.BEST_MATCH_VOLUNTEERS_LIMIT]
        serializer = MatchingVolunteerSerializer(queryset, many=True)

        return Response(serializer.data)


class HelpRequestsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = HelpRequest.objects.all().order_by('-created_date')
    serializer_class = HelpRequestSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = api.filters.HelpRequestsFilter
    throttle_classes = [api.throttling.HamalDataListThrottle]


class UpdateHelpRequestViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = HelpRequest.objects.all()
    serializer_class = UpdateHelpRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, *args, partial=False, **kwargs):
        return super().update(*args, **kwargs, partial=True)


class UpdateVolunteerViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = UpdateVolunteerSerializer
    permission_classes = [IsAuthenticated]

    def update(self, *args, partial=False, **kwargs):
        return super().update(*args, **kwargs, partial=True)


class VolunteerFreezeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = VolunteerFreezeSerializer
    permission_classes = [IsAuthenticated]


class HelpRequestMapViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = HelpRequest.objects.all()  # .filter(status__in=['WAITING', 'IN_CARE']).order_by('-created_date')
    serializer_class = MapHelpRequestSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = api.filters.HelpRequestsFilter
    throttle_classes = [api.throttling.HamalDataListThrottle]


class ListByNameViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = None

    def list(self, request, **kwargs):
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


class ExportVolunteersViewSet(viewsets.ViewSet):
    throttle_classes = [api.throttling.ExportExcelDataThrottle]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        volunteers = api.filters.VolunteerFilter(request.GET, queryset=Volunteer.objects.all()).qs
        current_time = datetime.now().strftime('%Y_%m_%d-%H%M%S')
        response = HttpResponse(VolunteerResource().export(volunteers).xls, 'application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Volunteers_data-{current_time}.xls"'

        return response


class ExportHelpRequestsViewSet(viewsets.ViewSet):
    throttle_classes = [api.throttling.ExportExcelDataThrottle]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        helprequests = api.filters.HelpRequestsFilter(request.GET, queryset=HelpRequest.objects.all()).qs
        current_time = datetime.now().strftime('%Y_%m_%d-%H%M%S')
        response = HttpResponse(HelpRequestResource().export(helprequests).xls, 'application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="HelpRequests_data-{current_time}.xls"'

        return response


class GetGoogleApiSecret(APIView):
    """
    return google maps GOOGLE_API_SECRET_KEY in JSON.
    """
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {'secret_key': settings.GOOGLE_API_SECRET_KEY}
        return Response(content)

