from django.urls import path
from . import views


urlpatterns = [
    path('volunteer_table', views.show_all_volunteers, name='show_all_volunteers'),
    path('help_table', views.show_all_help_request, name='show_all_help_request'),
    path('edit/<int:pk>', views.help_edit_stat, name='change_stat')
]