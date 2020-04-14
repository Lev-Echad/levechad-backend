from django.urls import include, path
from rest_framework import routers
import rest_framework.authtoken.views

import api.views

router = routers.DefaultRouter()
router.register(r'registration', api.views.RegistrationAPIViewSet, basename='registration')
router.register(r'volunteers', api.views.ListVolunteersViewSet, basename='volunteer_list')
router.register(r'sendverificationcode', api.views.SendVerificationCodeViewSet, basename='send_verification_code')
router.register(r'checkverificationcode', api.views.CheckVerificationCodeViewSet, basename='check_verification_code')


urlpatterns = [
    path('', include(router.urls)),
    path('authtoken', rest_framework.authtoken.views.obtain_auth_token),
    # path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
