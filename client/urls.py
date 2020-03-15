from django.urls import path
from . import views


urlpatterns = [
    path('', views.volunteer, name='show_all')
]