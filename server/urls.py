from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_all_volunteers, name='show_all')
]