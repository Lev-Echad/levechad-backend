from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from client.models import Volunteer, HelpRequest

def show_all_volunteers(request):
    qs = Volunteer.objects.all()
    print(request.POST)
    test = request.POST.get('test')
    if test is not None:
        qs = qs.filter(age=12)
    else:
        qs = qs.order_by('-full_name')
    context = {'volunteer_data': qs}
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


def show_all_help_request(request):
    all_help_requests = HelpRequest.objects.all()
    context = {'help_requests': all_help_requests}
    return render(request, 'server/help_table.html', context)