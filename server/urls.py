from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_all_volunteers, name='show_all'),
    path('', views.order_by_name, name='order_by_name')
]