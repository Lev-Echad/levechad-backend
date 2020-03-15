from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from client.models import Volunteer

def show_all_volunteers(request):
    all_volunteer_data = Volunteer.objects.all()
    context = {'all_volunteer_data': all_volunteer_data}
    return render(request, 'server/volunteer_table.html', context)

def order_by_name(request):
    all_volunteer_data = Volunteer.objects.all()
    all_volunteer_data_by_name = all_volunteer_data.order_by('-full_name')
    context = {'all_volunteer_data': all_volunteer_data_by_name}
    return render(request, 'server/volunteer_table.html', context)

# def order_by_age(request):
#     all_volunteer_data = Volunteer.objects.all()
#     all_volunteer_data_by_name = all_volunteer_data.order_by('age')
#     context = {'all_volunteer_data': all_volunteer_data_by_name}
#     return render(request, 'server/volunteer_table.html', context)