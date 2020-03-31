from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from client.models import Volunteer, HelpRequest, Area
from django.db.models import F, Q
from django.core.paginator import Paginator
import datetime
from datetime import time, date
from django.http import HttpResponse, HttpResponseBadRequest
import xlwt

RESULTS_IN_PAGE = 50


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def get_mandatory_areas(request):
    mandatory_areas = []

    if hasattr(request.user, 'hamaluser') and request.user.hamaluser is not None:
        area = request.user.hamaluser.area
        if area.name == "מרכז":
            mandatory_areas = Area.objects.all().filter(name__in=["ירושלים והסביבה", "מרכז", "יהודה ושומרון"])
        else:
            mandatory_areas = [area]

    return mandatory_areas


@login_required
def index(request):
    now = datetime.datetime.now()

    last_7am = datetime.datetime(now.year, now.month, now.day, 7, 0, 0)
    # If current time is before 7AM, get results for time since last 7AM (yesterday)
    if last_7am > now:
        last_7am = last_7am - datetime.timedelta(days=1)
    next_7am = last_7am + datetime.timedelta(days=1)

    # Filter requests by creation time.
    creation_timerange_filter = Q(created_date__range=(last_7am, next_7am))

    context = {
        "numbers": {
            "total_volunteers": Volunteer.objects.count(),
            "total_help_requests": HelpRequest.objects.count(),
            "solved_help_requests": HelpRequest.objects.filter(status="DONE").count()
        },
        "daily_numbers": {
            "daily_volunteers": Volunteer.objects.filter(
                creation_timerange_filter).count(),  # Tomorrow
            "daily_help": HelpRequest.objects.filter(creation_timerange_filter).count(),
            "daily_solved": HelpRequest.objects.filter(creation_timerange_filter, status="DONE").count()

        }
    }

    return render(request, 'server/server_index.html', context)


"""
also filters by filter
"""


@login_required
def show_all_volunteers(request, page=1):
    qs = Volunteer.objects.all()

    # ------- filters -------
    areas = request.GET.getlist('area')
    lans = request.GET.getlist('language')
    availability = request.GET.getlist('availability')
    guidings = request.GET.getlist('guiding')
    search_name = request.GET.getlist('searchname')
    something_mark = False

    area_qs = Volunteer.objects.all().none()
    language_qs = Volunteer.objects.all().none()
    availability_qs = Volunteer.objects.all().all()

    area_qs = qs
    if len(get_mandatory_areas(request)) != 0:
        area_qs = qs.filter(areas__name__in=get_mandatory_areas(request))

    if len(areas) != 0 and '' not in areas:
        something_mark = True
        area_qs = area_qs.filter(areas__name__in=areas)

    if len(lans) != 0 and '' not in lans:
        something_mark = True
        language_qs = qs.filter(languages__name__in=lans)

    if len(guidings) != 0:
        something_mark = True
        qs = qs.filter(guiding=True)

    if len(search_name) != 0:
        something_mark = True
        split_name = search_name[0].split()
        qs = qs.filter(Q(last_name=' '.join(split_name[1:])) | Q(first_name=split_name[0]))

    # --------- check time now --------
    now = datetime.datetime.now()
    now_day = now.strftime("%A")

    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    yesterday_day = yesterday.strftime("%A")

    # check option 1
    if is_time_between(time(7, 00), time(15, 00)):
        schedule_filter = "schedule__" + now_day + "__contains"
        availability_qs = qs.filter(**{schedule_filter: 1})

    # check option 2
    elif is_time_between(time(15, 00), time(23, 00)):
        schedule_filter = "schedule__" + now_day + "__contains"
        availability_qs = qs.filter(**{schedule_filter: 2})


    # check option 3 before midnight
    elif is_time_between(time(23, 00), time(00, 00)):
        schedule_filter = "schedule__" + now_day + "__contains"
        availability_qs = qs.filter(**{schedule_filter: 3})

    # check option 3 after midnight
    elif is_time_between(time(00, 00), time(7, 00)):
        schedule_filter = "schedule__" + yesterday_day + "__contains"
        availability_qs = qs.filter(**{schedule_filter: 3})

    availability_now_id = []
    if availability_qs != []:
        for volunteer in availability_qs:
            availability_now_id.append(volunteer.id)

    if len(availability) == 0:
        availability_qs = Volunteer.objects.all().all()

    # union matchings from both categoties
    match_qs = area_qs.union(language_qs)

    # if there were no matches display all and there are people available
    if len(match_qs) == 0 and (not something_mark):
        match_qs = Volunteer.objects.all()

    availability_qs = (availability_qs)
    match_qs = match_qs.intersection(availability_qs)

    # ----- orders -----
    if 'field' in request.GET:
        field = request.GET.get('field')
        field = "-" + field
        match_qs = match_qs.order_by(field)

    # ----- check for each volunteer how much times he apper
    appers_list = []
    valid_certificates = []
    for volunteer in match_qs:
        appers_list.append(HelpRequest.objects.filter(helping_volunteer=volunteer).count())
        volunteer.get_active_certificates()
        valid_certificate = volunteer.get_active_certificates().first()
        if valid_certificate is not None:
            valid_certificates.append(valid_certificate.id)
        else:
            valid_certificates.append(-1)

    # make match qs to tuple
    final_data = []
    for i in range(0, len(match_qs)):
        final_data.append((match_qs[i], appers_list[i], valid_certificates[i]))

    paginator = Paginator(final_data, RESULTS_IN_PAGE)

    final_data = paginator.page(page)

    context = {'volunteer_data': final_data, 'availability_now_id': availability_now_id, 'page': page,
               'num_pages': paginator.num_pages}
    return render(request, 'server/volunteer_table.html', context)


"""
also filters by filter
"""


@login_required
def show_all_help_request(request, page=1):
    qs = HelpRequest.objects.all()

    statuses = request.GET.getlist('status')
    type = request.GET.getlist('type')
    areas = request.GET.getlist('area')
    search_name = request.GET.getlist('search_name')

    something_mark = False

    status_qs = HelpRequest.objects.none()
    type_qs = HelpRequest.objects.none()
    area_qs = HelpRequest.objects.all().none()

    if len(statuses) != 0 and not '' in statuses:
        something_mark = True
        status_qs = qs.filter(status=statuses)

    if len(type) != 0 and not '' in type:
        something_mark = True
        type_qs = qs.filter(type__in=type)
    if len(get_mandatory_areas(request)) != 0:
        area_qs = area_qs.filter(area__name__in=get_mandatory_areas(request))

    if len(areas) != 0 and not '' in areas:
        something_mark = True
        area_qs = area_qs.filter(area__name__in=areas)

    if len(search_name) != 0:
        something_mark = True
        qs = qs.filter(full_name=search_name[0])

    # union matchings from both categoties
    match_qs = status_qs.union(type_qs, area_qs)

    # if there were no matches display all
    if len(match_qs) == 0 and (not something_mark):
        match_qs = HelpRequest.objects.all()

    match_qs = match_qs.order_by("-id")
    paginator = Paginator(match_qs, RESULTS_IN_PAGE)
    match_qs = paginator.page(page)

    context = {'help_requests': match_qs, 'page': page, 'num_pages': paginator.num_pages}
    return render(request, 'server/help_table.html', context)


"""
also filters by filter
"""


@login_required
def order_help_request(request):
    qs = HelpRequest.objects.all()
    statuses = request.POST.getlist('status')
    type = request.POST.getlist('type')

    status_qs = HelpRequest.objects.none()
    type_qs = HelpRequest.objects.none()

    if len(statuses) != 0:
        status_qs = qs.filter(status__in=statuses)

    if len(type) != 0:
        type_qs = qs.filter(type__in=type)

    # union matchings from both categoties
    match_qs = status_qs.union(type_qs)

    # if there were no matches display all
    if len(match_qs) == 0:
        match_qs = qs

    context = {'help_requests': match_qs}
    return render(request, 'server/help_table.html', context)


@login_required
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
            # adding new certificate
            volunteer_to_add.get_or_generate_valid_certificate()
            to_edit.helping_volunteer = volunteer_to_add
        except Volunteer.DoesNotExist:
            pass
        except ValueError:
            pass

    to_edit.save()
    return redirect('show_all_help_request')


@login_required
def volunteer_edit_notes(request, pk):
    to_edit = Volunteer.objects.get(id=pk)
    if request.POST.get('notes') is not None:
        to_edit.notes = request.POST.get('notes')
    to_edit.save()
    return redirect('show_all_volunteers')


@login_required
def delete_volunteer(request, pk):
    to_delete = Volunteer.objects.get(id=pk)
    to_delete.delete()
    return redirect('show_all_volunteers')


@login_required
def find_closes_persons(request, pk):
    request_person = HelpRequest.objects.get(id=pk)

    req_city = request_person.city
    req_x = req_city.x
    req_y = req_city.y

    closest_volunteer = Volunteer.objects.all()

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
        availability_qs = closest_volunteer.filter(**{filter: 1})

    # check option 2
    elif is_time_between(time(15, 00), time(23, 00)):
        filter = "schedule__" + now_day + "__contains"
        availability_qs = closest_volunteer.filter(**{filter: 2})


    # check option 3 before midnight
    elif is_time_between(time(23, 00), time(00, 00)):
        filter = "schedule__" + now_day + "__contains"
        availability_qs = closest_volunteer.filter(**{filter: 3})

    # check option 3 after midnight
    elif is_time_between(time(00, 00), time(7, 00)):
        filter = "schedule__" + yesterday_day + "__contains"
        availability_qs = closest_volunteer.filter(**{filter: 3})

    # check for the persons that good timing if the day is good

    availability_now_id = []
    if availability_qs != []:
        for volu in availability_qs:
            availability_now_id.append(volu.id)

    closest_volunteer = availability_qs

    closest_volunteer = sorted(closest_volunteer,
                              key=lambda volu: -HelpRequest.objects.filter(helping_volunteer=volu).count())
    closest_volunteer = sorted(closest_volunteer,
                              key=lambda volu: (volu.city.x - req_x) ** 2 + (volu.city.y - req_y) ** 2)

    # closest_volunteer = closest_volunteer.order_by((F('city__x')-req_x)**2 + (F('city__y')-req_y)**2)

    if len(closest_volunteer) > 100:
        closest_volunteer = closest_volunteer[0:100]

    # ----- check for each volunteer how much times he apper
    appers_list = []
    for volu in closest_volunteer:
        appers_list.append(HelpRequest.objects.filter(helping_volunteer=volu).count())

    final_data = []
    for i in range(0, len(closest_volunteer)):
        tot_x = (closest_volunteer[i].city.x - request_person.city.x) ** 2
        tot_y = (closest_volunteer[i].city.y - request_person.city.y) ** 2
        tot_value = int(((tot_x + tot_y) ** 0.5) / 100)
        final_data.append((closest_volunteer[i], tot_value, appers_list[i]))

    context = {'help_request': request_person, 'closest_volunteer': final_data,
               'availability_now_id': availability_now_id}
    return render(request, 'server/closest_volunteer.html', context)


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="volunteer_data.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Volunteers')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['שם', 'שם פרטי', 'שם משפחה', 'תעודת זהות', 'סוג', 'גיל', 'טלפון', 'שפות' 'שם משפחה', 'איזור', 'עיר',
               'אימייל', 'פנוי בשבת',
               'משפחותונים', 'Notes', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Volunteer.objects.all().values_list('full_name', 'first_name', 'last_name', 'tz_number', 'volunteer_type',
                                               'age',
                                               'phone_number', 'areas', 'city', 'email', 'available_saturday',
                                               'guiding', 'notes')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


@login_required
def create_volunteer_certificate(request, volunteer_id):
    try:
        volunteer = Volunteer.objects.get(id=volunteer_id)
        certificate = volunteer.get_or_generate_valid_certificate()
    except Volunteer.DoesNotExist:
        return HttpResponseBadRequest()

    return redirect('volunteer_certificate', pk=certificate.id)


def export_help_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="help_request_data.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('HelpRequests')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['שם פונה', 'טלפון', 'איזור', 'כתובת' 'עיר', 'סוג פנייה', 'הערות', 'סטטוס', 'מתנדב שמפטל']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = HelpRequest.objects.all().values_list('full_name', 'phone_number', 'area', 'address', 'city', 'type',
                                                 'notes', 'status', 'helping_volunteer')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
