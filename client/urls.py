from django.urls import path
from . import views


urlpatterns = [
    path('volunteer', views.volunteer, name='show_all'),
    path('buy_in', views.buy_in, name='show_all'),
    path('medic', views.medic, name='show_all'),
    path('volunteer', views.volunteer, name='show_all'),
    path('get_help', views.first_help, name='show_all'),
    path('schedule', views.schedule, name='show_all'),
    path('thanks', views.thanks, name='show_all'),
    path('', views.homepage, name='show_all')
]