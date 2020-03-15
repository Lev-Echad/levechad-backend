from django.urls import path
from . import views


urlpatterns = [
#     path('buy_in', views.buy_in, name='show_all'),
#     path('medic', views.medic, name='show_all'),
#     path('schedule', views.schedule, name='show_all'),
    path('', views.homepage, name='show_all'),
    path('get_help', views.get_help, name='show_all'),
    path('send_help', views.send_help, name='show_all'),
    path('thanks', views.thanks, name='show_all'),

    path('help/shopping', views.shopping_help, name='show_all'),

]