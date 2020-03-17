from django.shortcuts import render, redirect
from client.models import Volunteer, HelpRequest
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
    areas = request.POST.getlist('area')
    lans = request.POST.getlist('language')
    availability = request.POST.getlist('availability')

    something_mark = False

    area_qs=Volunteer.objects.all().none()
    language_qs=Volunteer.objects.all().none()
    availability_qs=Volunteer.objects.all().all()

    if len(areas) != 0 and not '' in areas:

        something_mark = True
        area_qs = qs.filter(areas__name__in=areas)


    if len(lans) != 0 and not '' in lans:

        something_mark = True
        language_qs = qs.filter(languages__name__in=lans)


    # --------- check time now --------
    now = datetime.datetime.now()
    now_day = now.strftime("%A")

    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    yesterday_day = yesterday.strftime("%A")

    # check option 1
    if is_time_between(time(7, 00), time(15, 00)):
        filter = "schedule__" + now_day + "__contains"
        availability_qs = qs.filter(**{filter:1})

    # check option 2
    elif is_time_between(time(15, 00), time(23, 00)):
        filter = "schedule__" + now_day + "__contains"
        availability_qs = qs.filter(**{filter:2})


    # check option 3 before midnight
    elif is_time_between(time(23, 00), time(00, 00)):
        filter = "schedule__" + now_day + "__contains"
        availability_qs = qs.filter(**{filter:3})

    # check option 3 after midnight
    elif is_time_between(time(00, 00), time(7, 00)):
        filter = "schedule__" + yesterday_day + "__contains"
        availability_qs = qs.filter(**{filter:3})


    availability_now_id = []
    if availability_qs != []:
        for volu in availability_qs:
            availability_now_id.append(volu.id)




    if len(availability) == 0:
        availability_qs = Volunteer.objects.all().all()


    # union matchings from both categoties
    match_qs = area_qs.union(language_qs)

    guidings1 = request.POST.getlist('guiding')


    # if there were no matches display all and there are people available
    if len(match_qs) == 0 and (not something_mark):
        match_qs = Volunteer.objects.all()

    if len(guidings1) != 0:
        match_qs = match_qs.filter(guiding=True)

    availability_qs = (availability_qs)
    match_qs = match_qs.intersection(availability_qs)


    # ----- orders -----
    if 'field' in request.POST:
        field = request.POST.get('field')
        match_qs = match_qs.order_by(field)



    #----- check for each volunterr how much times he apper
    appers_list = []
    for volu in match_qs:
        appers_list.append(HelpRequest.objects.filter(helping_volunteer=volu).count())

    # make match qs to tuple
    final_data = []
    for i in range (0, len(match_qs)):
        final_data.append((match_qs[i], appers_list[i]))


    context = {'volunteer_data': final_data, 'availability_now_id': availability_now_id}
    return render(request, 'server/volunteer_table.html', context)

"""
also filters by filter
"""
def show_all_help_request(request):
    qs = HelpRequest.objects.all()

    statuses = request.POST.getlist('status')
    type = request.POST.getlist('type')


    something_mark = False

    status_qs =HelpRequest.objects.none()
    type_qs = HelpRequest.objects.none()

    if len(statuses) != 0 and not '' in statuses:
        something_mark = True
        status_qs = qs.filter(status__in=statuses)

    if len(type) != 0 and not '' in type:
        something_mark = True
        type_qs = qs.filter(type__in=type)

    # union matchings from both categoties
    match_qs = status_qs.union(type_qs)

    # if there were no matches display all
    if len(match_qs) == 0 and (not something_mark):
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
    statuses = request.POST.getlist('status')
    type = request.POST.getlist('type')


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

    if request.POST.get('notes') is not None:
        to_edit.notes = request.POST.get('notes')

    if request.POST.get('volunteer_id') is not None:
        volunteer_id = request.POST.get('volunteer_id')

        # check if this volunteer exist
        try:
            volunteer_to_add = Volunteer.objects.get(id=volunteer_id)
            to_edit.helping_volunteer = volunteer_to_add
        except:
            pass


    to_edit.save()
    return redirect('show_all_help_request')




def volunteer_edit_notes(request, pk):
    to_edit = Volunteer.objects.get(id=pk)
    if request.POST.get('notes') is not None:
        to_edit.notes = request.POST.get('notes')
    to_edit.save()
    return redirect('show_all_volunteers')




def find_closes_persons(request, pk):
    request_person = HelpRequest.objects.get(id=pk)

    req_city = request_person.city
    req_x =  req_city.x
    req_y = req_city.y

    closes_volunteer = Volunteer.objects.all()
    closes_volunteer = closes_volunteer.order_by((F('city__x')-req_x)**2 + (F('city__y')-req_y)**2)



    # adding here a function that tell if the volunteer is aviavble
    # --------- check time now --------
    now = datetime.datetime.now()
    now_day = now.strftime("%A")

    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    yesterday_day = yesterday.strftime("%A")

    availability_qs = []

    # check option 1
    if is_time_between(time(7, 00), time(15, 00)):
        filter = "schedule__" + now_day + "__contains"
        availability_qs = closes_volunteer.filter(**{filter: 1})

    # check option 2
    elif is_time_between(time(15, 00), time(23, 00)):
        filter = "schedule__" + now_day + "__contains"
        availability_qs = closes_volunteer.filter(**{filter: 2})


    # check option 3 before midnight
    elif is_time_between(time(23, 00), time(00, 00)):
        filter = "schedule__" + now_day + "__contains"
        availability_qs = closes_volunteer.filter(**{filter: 3})

    # check option 3 after midnight
    elif is_time_between(time(00, 00), time(7, 00)):
        filter = "schedule__" + yesterday_day + "__contains"
        availability_qs = closes_volunteer.filter(**{filter: 3})

    # check for the persons that good timing if the day is good

    availability_now_id = []
    if availability_qs != []:
        for volu in availability_qs:
            availability_now_id.append(volu.id)

    closes_volunteer = availability_qs

    if len(closes_volunteer) > 30:
        closes_volunteer = closes_volunteer[0:29]

    final_data = []
    for volunteer in closes_volunteer:
        tot_x = (volunteer.city.x - request_person.city.x) ** 2
        tot_y = (volunteer.city.y - request_person.city.y) ** 2
        tot_value = int(((tot_x + tot_y) ** 0.5) / 100)
        final_data.append((volunteer, tot_value))

    context = {'help_request': request_person, 'closes_volunteer': final_data, 'availability_now_id': availability_now_id}
    return render(request, 'server/closes_volunteer.html', context)