import re

from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from client.models import Volunteer
from api.serializers import VolunteerSerializer, RegistrationSerializer

INVALID_PHONE_CHARACTER_REGEX = r'[^0-9\-+]'
MAX_PHONE_NUMBER_LENGTH = 20
MIN_PHONE_NUMBER_LENGTH = 9


class SendVerificationCodeViewSet(viewsets.ViewSet):
    def create(self, request):
        def _is_valid_phone_number(string):
            # TODO add better validation, make the client forms & this one use the same phone validation after refactor
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


class ListVolunteersViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Volunteer.objects.all().order_by('-created_date')
    serializer_class = VolunteerSerializer
    permission_classes = [IsAuthenticated]
