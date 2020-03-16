from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from client.models import Volunteer, HelpRequest


def index(request):
    context = {}
    return render(request, 'server/server_index.html', context)


def show_all_volunteers(request):
    qs = Volunteer.objects.all()
    print(request.POST)
    areas = request.POST.getlist('area')
    lans = request.POST.getlist('language')
    print("areas: "+str(areas))
    print("languages: " + str(lans))
    if areas is not None:
        print("area")
        temp_qs = qs.filter(area__in = areas)
        # check there were matches
        if len(temp_qs) != 0:
            qs = temp_qs
        print(qs)
    if lans is not None:
        print("lan")
        print(lans)
        # check there were matches
        temp_qs = qs.filter(languages__name__in=lans)
        if len(temp_qs) != 0:
            qs = temp_qs
        print(qs)


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


def help_edit_stat(request, pk):
    # get user objects
    print(request.POST)
    to_edit = HelpRequest.objects.get(id=pk)
    print(to_edit.status)

    if request.POST.get('status') is not None:
        to_edit.status = request.POST.get('status')

    if request.POST.get('user_name') is not None:
        to_edit.status_updater = request.POST.get('user_name')

    print(to_edit.status)
    to_edit.save()
    return redirect('show_all_help_request')