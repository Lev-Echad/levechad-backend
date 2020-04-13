import re
from operator import gt, lt, eq

from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import VolunteerSerializer, RegistrationSerializer
from client.models import Volunteer

INVALID_PHONE_CHARACTER_REGEX = r'[^0-9\-+]'
MAX_PHONE_NUMBER_LENGTH = 20
MIN_PHONE_NUMBER_LENGTH = 9


class SendVerificationCodeViewSet(viewsets.ViewSet):
    def create(self, request):
        def _is_valid_phone_number(string):
            # TODO think of better validation, make the client forms & this one use the same phone validation after refactor
            return len(re.findall(INVALID_PHONE_CHARACTER_REGEX, string)) == 0 and \
                   MIN_PHONE_NUMBER_LENGTH <= len(string) <= MAX_PHONE_NUMBER_LENGTH

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

        # TODO STUB - Implement in #198
        return Response({'success': True, 'message': ''})


class CheckVerificationCodeViewSet(viewsets.ViewSet):
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

        # TODO STUB - Implement in #198
        return Response({'success': True, 'message': ''})


class RegistrationAPIViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = RegistrationSerializer


class VolunteerFilter(filters.FilterSet):
    OPERATORS = {"eq": eq, "gt": gt, "lt": lt}

    times_volunteered = filters.NumberFilter(method='get_times_volunteered', field_name='eq')
    times_volunteered__gt = filters.NumberFilter(method='get_times_volunteered', field_name='gt')
    times_volunteered__lt = filters.NumberFilter(method='get_times_volunteered', field_name='lt')

    def get_times_volunteered(self, queryset, field_name, value):
        if value and field_name in self.OPERATORS.keys():
            ids = [volunteer.id for volunteer in queryset if
                   self.OPERATORS[field_name](volunteer.times_volunteered, value)]
            return queryset.filter(id__in=ids)
        return queryset

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


class ListVolunteersViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Volunteer.objects.all().order_by('-created_date')
    serializer_class = VolunteerSerializer
    permission_classes = [AllowAny]
    filterset_class = VolunteerFilter
