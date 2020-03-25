from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('volunteer_table', views.show_all_volunteers, name='show_all_volunteers'),
    path('volunteer_table/<int:page>', views.show_all_volunteers, name='show_all_volunteers_page'),
    path('help_table', views.show_all_help_request, name='show_all_help_request'),
    path('help_table/<int:page>', views.show_all_help_request, name='show_all_help_request_page'),
    path('edit/<int:pk>', views.help_edit_stat, name='change_stat'),
    path('find_closes/<int:pk>', views.find_closes_persons, name='find_closes_persons'),
    path('edit_note/<int:pk>', views.volunteer_edit_notes, name='volunteer_edit_notes'),  
    path('delete_volunteer/<int:pk>', views.delete_volunteer, name='delete_volunteer'),
    path(r'export/xls/', views.export_users_xls, name='export_users_xls'),
    path(r'export/xls1/', views.export_help_xls, name='export_help_xls'),

]
