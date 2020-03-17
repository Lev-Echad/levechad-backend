from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('volunteer_table', views.show_all_volunteers, name='show_all_volunteers'),
    path('help_table', views.show_all_help_request, name='show_all_help_request'),
    path('edit/<int:pk>', views.help_edit_stat, name='change_stat'),
    path('find_closes/<int:pk>', views.find_closes_persons, name='find_closes_persons'),
    path('edit_note/<int:pk>', views.volunteer_edit_notes, name='volunteer_edit_notes')
]