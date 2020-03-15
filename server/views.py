from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from client.models import Volunteer

def show_all_volunteers(request):
    all_volunteer_data = Volunteer.objects.all()
    context = {'all_volunteer_data': all_volunteer_data}
    return render(request, 'server/volunteer_table.html', context)


