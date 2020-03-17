from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='show_all'),
    path('home', views.homepage, name='show_all'),
    path('thanks', views.thanks, name='show_all'),

    path('volunteer', views.volunteer, name='show_all'),
    path('schedule', views.schedule, name='show_all'),

    path('get_help', views.get_help, name='show_all'),
    path('help/home', views.home_help, name='show_all'),
    path('help/medic', views.medic_help, name='show_all'),
    path('help/other', views.other_help, name='show_all'),
    path('help/phone', views.phone_help, name='show_all'),
    path('help/shopping', views.shopping_help, name='show_all'),
    path('help/travel', views.travel_help, name='show_all'),
]
