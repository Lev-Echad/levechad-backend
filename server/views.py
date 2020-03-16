from django.shortcuts import render, redirect
from client.models import Volunteer, HelpRequest, Area
from django.db.models import F
import datetime
from datetime import  time


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def index(request):
    context = {}
    return render(request, 'server/server_index.html', context)

"""
also filters by filter
"""
def show_all_volunteers(request):
    qs = Volunteer.objects.all()



    # ------- filters -------
    print("post: ")
    print(request.POST)
    areas = request.POST.getlist('area')
    lans = request.POST.getlist('language')
    availability = request.POST.getlist('availability')
    print("areas: "+str(areas))
    print("languages: " + str(lans))
    print("availability: " + str(availability))

    area_qs =  Volunteer.objects.all().none()
    language_qs =  Volunteer.objects.all().none()
    availability_qs =  Volunteer.objects.all().all()

    if len(areas) != 0 :

        area_qs = qs.filter(areas__name__in=areas)
        print(area_qs)

    if len(lans) != 0 :
        language_qs = qs.filter(languages__name__in=lans)
        print(language_qs)


    # --------- check time now
    now = datetime.datetime.now()
    now_day = now.strftime("%A")

    yesterday = datetime.datetime.today() + datetime.timedelta(days=-1)
    yesterday_day = yesterday.strftime("%A")
    #

    if len(availability) != 0:
        # check option 1
        if is_time_between(time(7, 00), time(15, 00)):
            filter = "schedule__" + now_day
            availability_qs = qs.filter(**{filter:1})

        # check option 2
        elif is_time_between(time(15, 00), time(23, 00)):
            filter = "schedule__" + now_day
            availability_qs = qs.filter(**{filter:2})


        # check option 3 before midnight
        elif is_time_between(time(23, 00), time(00, 00)):
            filter = "schedule__" + now_day
            availability_qs = qs.filter(**{filter:3})

        # check option 3 after midnight
        elif is_time_between(time(00, 00), time(7, 00)):
            filter = "schedule__" + yesterday_day
            availability_qs = qs.filter(**{filter: 3})

    # union matchings from both categoties
    match_qs = area_qs.union(language_qs)
    print("before date")
    print(match_qs)
    match_qs = match_qs.intersection(availability_qs)
    print("after intersection")
    print(match_qs)

    # if there were no matches display all and there are people available
    if len(match_qs) == 0 and len(availability_qs) !=0:
        print("no match")
        print(availability_qs)
        match_qs = availability_qs

    # # ----- orders -----
    # if 'field' in request.POST:
    #     field = request.POST.get('field')
    #     match_qs = match_qs.order_by(field)



    context = {'volunteer_data': match_qs}
    return render(request, 'server/volunteer_table.html', context)

"""
also filters by filter
"""
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


"""
also filters by filter
"""
def order_help_request(request):
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