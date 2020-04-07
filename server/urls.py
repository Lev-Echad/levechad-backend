from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('volunteer_table/', views.show_all_volunteers, name='show_all_volunteers'),
    path('help_table/', views.show_all_help_request, name='show_all_help_request'),
    path('edit/', views.help_edit_stat, name='change_stat'),
    path('find_closes/', views.find_closes_persons, name='find_closes_persons'),
    path('edit_note/', views.volunteer_edit_notes, name='volunteer_edit_notes'),
    path('edit_tz/', views.volunteer_edit_tz_num, name="volunteer_edit_tz_num"),
    path('edit_city/', views.volunteer_edit_city, name="volunteer_edit_city"),
    path('edit_type/', views.volunteer_edit_type, name='volunteer_edit_type'),
    path('create_volunteer_certificate/', views.create_volunteer_certificate, name='create_volunteer_certificate'),

    path('delete_volunteer/', views.delete_volunteer, name='delete_volunteer'),
    path('export/xls/', views.export_users_xls, name='export_users_xls'),
    path('export/xls1/', views.export_help_xls, name='export_help_xls'),

]
