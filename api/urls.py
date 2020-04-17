from django.urls import include, path
from rest_framework import routers

import api.views

router = routers.DefaultRouter()
router.register(r'registration', api.views.RegistrationViewSet, basename='registration')
router.register(r'createhelprequest', api.views.CreateHelpRequestViewSet, basename='create_help_request')
router.register(r'volunteers', api.views.ListVolunteersViewSet, basename='volunteer_list')
router.register(r'helprequests', api.views.ListHelpRequestsViewSet, basename='help_request_list')
router.register(r'sendverificationcode', api.views.SendVerificationCodeViewSet, basename='send_verification_code')
router.register(r'checkverificationcode', api.views.CheckVerificationCodeViewSet, basename='check_verification_code')


urlpatterns = [
    path('', include(router.urls)),
    path('authtoken', api.views.CustomAuthToken.as_view()),
]
