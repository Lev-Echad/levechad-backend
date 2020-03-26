from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage),
    path('home', views.homepage),
    path('thanks', views.thanks),
    path('thanks_volunteer', views.thanks_volunteer),

    path('volunteer', views.volunteer_view),
    path('schedule', views.schedule),

    path('get_help', views.get_help),
    path('help/home', views.home_help),
    path('help/medic', views.medic_help),
    path('help/other', views.other_help),
    path('help/phone', views.phone_help),
    path('help/shopping', views.shopping_help),
    path('help/travel', views.travel_help),
    path('help/workers', views.workers_help),
    path('volunteer_certificate/<int:pk>', views.volunteer_certificate_view, name='volunteer_certificate'),
]
