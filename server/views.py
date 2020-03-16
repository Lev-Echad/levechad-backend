from django.shortcuts import render, redirect
from client.models import Volunteer, HelpRequest
from django.db.models import F

def index(request):
    context = {}
    return render(request, 'server/server_index.html', context)


def show_all_volunteers(request):
    qs = Volunteer.objects.all()

    # ------- filters -------
    print("post: ")
    print(request.POST)
    areas = request.POST.getlist('area')
    lans = request.POST.getlist('language')
    print("areas: "+str(areas))
    print("languages: " + str(lans))

    area_qs = HelpRequest.objects.none()
    language_qs = HelpRequest.objects.none()

    if len(areas) != 0 :
        area_qs = qs.filter(area__in=areas)

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


    # ----- orders -----
    if 'field' in request.POST:
        field = request.POST.get('field')
        match_qs = match_qs.order_by(field)


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

    req_city = request_person.city
    req_x =  req_city.x
    req_y = req_city.y

    closes_volunteer = Volunteer.objects.all()
    closes_volunteer = closes_volunteer.order_by((F('city__x')-req_x)**2 + (F('city__y')-req_y)**2)

    final_data = []
    for volunteer in closes_volunteer:
        tot_x = (volunteer.city.x - request_person.city.x) ** 2
        tot_y = (volunteer.city.y - request_person.city.y) ** 2
        tot_value = int(((tot_x + tot_y) ** 0.5) / 100)
        final_data.append((volunteer, tot_value))

    context = {'help_request': request_person, 'closes_volunteer': final_data}
    return render(request, 'server/closes_volunteer.html', context)