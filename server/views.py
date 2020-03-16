from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from client.models import Volunteer, HelpRequest


def index(request):
    context = {}
    return render(request, 'server/server_index.html', context)


def show_all_volunteers(request):
    qs = Volunteer.objects.all()
    print("post: ")
    print(request.POST)
    areas = request.POST.getlist('area')
    lans = request.POST.getlist('language')
    print("areas: "+str(areas))
    print("languages: " + str(lans))

    area_qs = HelpRequest.objects.none()
    language_qs = HelpRequest.objects.none()

    if len(areas) != 0 :
        area_qs = qs.filter(area__in = areas)

    if len(lans) != 0 :
        language_qs = qs.filter(languages__name__in=lans)

    # union matchings from both categoties
    match_qs = area_qs.union(language_qs)

    # if there were no matches display all
    if len(match_qs) == 0:
        match_qs = qs


    context = {'volunteer_data': match_qs}
    return render(request, 'server/volunteer_table.html', context)


def show_all_help_request(request):
    qs = HelpRequest.objects.all()
    print("post:")
    print(request.POST)
    statuses = request.POST.getlist('status')
    type = request.POST.getlist('type')
    print("status: " + str(statuses))
    print("type: " + str(type))

    status_qs =HelpRequest.objects.none()
    type_qs = HelpRequest.objects.none()

    if len(statuses) != 0 :
        status_qs = qs.filter(status__in=statuses)

    if len(type) != 0:
        type_qs = qs.filter(type__in=type)

    # union matchings from both categoties
    match_qs = status_qs.union(type_qs)

    # if there were no matches display all
    if len(match_qs) ==0:
        match_qs = qs

    context = {'help_requests': match_qs}
    return render(request, 'server/help_table.html', context)


def help_edit_stat(request, pk):
    # get user objects
    to_edit = HelpRequest.objects.get(id=pk)

    if request.POST.get('status') is not None:
        to_edit.status = request.POST.get('status')

    if request.POST.get('user_name') is not None:
        to_edit.status_updater = request.POST.get('user_name')

    to_edit.save()
    return redirect('show_all_help_request')


def find_closes_persons(request, pk):
    request_person = HelpRequest.objects.get(id=pk)

    closes_volunteer = Volunteer.objects.all()

    context = {'help_request': request_person, 'closes_volunteer': closes_volunteer}
    return render(request, 'server/closes_volunteer.html', context)