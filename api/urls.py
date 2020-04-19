from django.urls import include, path
from rest_framework import routers

import api.views

router = routers.DefaultRouter()
router.register(r'registration', api.views.RegistrationViewSet, basename='registration')
router.register(r'createhelprequest', api.views.CreateHelpRequestViewSet, basename='create_help_request')
router.register(r'volunteers', api.views.VolunteersViewSet, basename='volunteer_list')
router.register(r'helprequests', api.views.HelpRequestsViewSet, basename='help_request_list')
router.register(r'maphelprequests', api.views.HelpRequestMapViewSet, basename='map_help_request_list')
router.register(r'updatehelprequest', api.views.UpdateHelpRequestViewSet, basename='update_help_request_list')
router.register(r'cityautocomplete', api.views.CityAutocompleteViewSet, basename='city_autocomplete')
router.register(r'areas', api.views.AreasViewSet, basename='area_list')
router.register(r'languages', api.views.LanguagesViewSet, basename='language_list')
router.register(r'sendverificationcode', api.views.SendVerificationCodeViewSet, basename='send_verification_code')
router.register(r'checkverificationcode', api.views.CheckVerificationCodeViewSet, basename='check_verification_code')


urlpatterns = [
    path('', include(router.urls)),
    path('getGoogleApiSecret/', api.views.GetGoogleApiSecret.as_view()),
    path('authtoken/', api.views.CustomAuthToken.as_view()),
]
