from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import *
from .models import Volunteer, City, Language, VolunteerSchedule, VolunteerCertificate, HelpRequest, Area
from django.db.models.functions import Concat
from django.db.models import Value, CharField, F


def thanks(request):
    try:
        username = request.GET['username']
        pk = request.GET['pk']

        hr = HelpRequest.objects.get(pk=pk, full_name=username)

        return render(request, 'thanks.html', {
            "id": pk,
            "message": "סטאטוס הבקשה שלך בLIVE",
            "status": str(hr.get_status_display())

        })
    except Exception as e:
        return render(request, 'thanks.html', {
            "id": " ",
            "message": "התקשר למוקד שלנו לפרטים נוספים",
            "status": ""
        })


def thanks_volunteer(request):
    volunteer_id = request.GET['vol_id']
    volunteer = Volunteer.objects.get(id=volunteer_id)
    volunteer_certificate = volunteer.get_active_certificates().first()

    return render(request, 'thanks_volunteer.html', {
        "name": f'{volunteer.first_name} {volunteer.last_name}',
        "certificate": volunteer_certificate
    })


def homepage(request):
    context = {
        "numbers": {
            "total_volunteers": Volunteer.objects.count() + 1786,
            "total_help_requests": HelpRequest.objects.count() + 84
            # added 1786 and 84 since those are the stats for before this app

        }
    }

    return render(request, 'index.html', context)


def get_help(request):
    return render(request, 'get_help.html', {})


def volunteer_view(request):
    # if this is a POST request we need to process the form data
    organization = request.GET.get('org', '')
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data
            languages = Language.objects.filter(name__in=answer["languages"])
            areas = Area.objects.filter(name__in=answer["area"])

            volunteer_new = Volunteer.objects.create(
                tz_number=answer["id_number"],
                first_name=answer["first_name"],
                last_name=answer["last_name"],
                email=answer["email"],
                date_of_birth=answer["date_of_birth"],
                organization=answer['organization'],
                phone_number=answer["phone_number"],
                city=City.objects.get(name=answer["city"]),
                neighborhood=answer['neighborhood'],
                address=answer["address"],
                available_saturday=answer["available_on_saturday"],
                notes=answer["notes"],
                moving_way=answer["transportation"],
                hearing_way=answer["hearing_way"],
                keep_mandatory_worker_children=(answer["childrens"] == "YES"),
                guiding=False
            )
            volunteer_new.languages.set(languages)
            volunteer_new.areas.set(areas)

            # creating volunteer certificate
            volunteer_new.get_or_generate_valid_certificate()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # TODO Don't hardcode URLs, get them by view
            return HttpResponseRedirect('/client/schedule?vol_id=' + str(volunteer_new.pk))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = VolunteerForm(initial={'organization': organization})

    return render(request, 'volunteer.html', {'form': form, 'organization': organization})


def schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            answer = form.cleaned_data
            new_schedule = VolunteerSchedule(Sunday="".join(answer["sunday"]), Monday="".join(answer["monday"]),
                                             Tuesday="".join(answer["tuesday"]), Wednesday="".join(answer["wednesday"]),
                                             Thursday="".join(answer["thursday"]), Friday="".join(answer["friday"]),
                                             Saturday="".join(answer["saturday"]))
            volunteerSchedule = Volunteer.objects.get(id=int(request.POST.get('vol_id', '')))
            new_schedule.save()
            volunteerSchedule.schedule = new_schedule
            volunteerSchedule.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            vol_pk = request.POST['vol_id']

            return HttpResponseRedirect('/client/thanks_volunteer?vol_id=' + str(vol_pk))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ScheduleForm()

    return render(request, 'schedule.html', {'form': form, 'id': request.GET.get('vol_id', '')})


def find_certificate_view(request):
    context = {}
    form = GetCertificateForm()
    if request.method == 'POST':
        form = GetCertificateForm(request.POST)
        if form.is_valid():
            # TODO: change to 'get' instead of 'first' after fixing #50
            volunteers_qs = Volunteer.objects.all()
            volunteers_qs = volunteers_qs.annotate(calc_full_name=Concat(F('first_name'), Value(' '), F('last_name'),
                                                                         output_field=CharField()))
            volunteers_qs = volunteers_qs.filter(tz_number__exact=form['id_number'].data)
            volunteers_qs = volunteers_qs.filter(calc_full_name__iexact=form['signing'].data)
            volunteer = volunteers_qs.first()
            if volunteer is not None:
                '''
                 TODO: this a hotfix that generate a valid certificate to any user that requests one. 
                 it should be reverted to the commented part  when #52 is solved
                '''
                # active_certificate = volunteer.get_active_certificates().first()
                active_certificate = volunteer.get_or_generate_valid_certificate()

                if active_certificate is not None:
                    context['certificate'] = active_certificate
                else:
                    context['error'] = 'לא נמצאה תעודה בתוקף!'
            else:
                context['error'] = 'מתנדב לא נמצא, האם מילאת את הפרטים כמו שצריך?'
        else:
            context['error'] = 'יש למלא את השדות כנדרש!'
    context['form'] = form
    return render(request, 'find_certificate.html', context=context)


def download_certificate_view(request, pk):
    # We could've easily used the download attribute on <a> tags w/ the media URL directly,
    # but this doesn't work on Firefox for some reason.
    # This is only for development purposes - see VolunteerCertificate.image_download_url
    with open(VolunteerCertificate.objects.get(id=pk).image.path, 'rb') as image_file:
        response = HttpResponse(image_file.read(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="{}.png"'.format(pk)
        return response


# === HELP VIEWS ===
def help_view(request, template_path, form_class, request_type_name, type_text_gen):
    """
    A generic help view that can be extended by the specific help views.
    :param request: The request as received from django
    :param template_path: The path to the template of this help request view
    :param form_class: The class of the form used (in forms.py)
    :param request_type_name: The string type of the request (keys of HelpRequest.TYPES)
    :param type_text_gen: A function that takes the answer (list, form.cleaned_data) and returns the type_text field
    """
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            answer = form.cleaned_data
            areas = Area.objects.all().get(name=answer['area'])

            new_request = HelpRequest(
                full_name=answer['full_name'],
                phone_number=answer['phone_number'],
                city=City.objects.get(name=answer['city']),
                address=answer['address'],
                notes=answer['notes'],
                type=request_type_name,
                request_reason=answer['request_reason'],
                type_text=type_text_gen(answer),
                area=areas
            )
            new_request.save()

            return HttpResponseRedirect('/client/thanks?username=' + answer["full_name"] + "&pk=" + str(new_request.pk))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = form_class()

    return render(request, template_path, {'form': form})


def shopping_help(request):
    return help_view(
        request,
        'help_pages/shopping.html',
        ShoppingForm,
        'BUYIN',
        lambda answer: answer['to_buy']
    )


def medic_help(request):
    def generate_type_text(answer):
        type_text = ''
        if answer['need_prescription']:
            type_text = 'תרופת מרשם\n'
        return type_text + answer['medic_name']

    return help_view(
        request,
        'help_pages/medic.html',
        MedicForm,
        'MEDICI',
        generate_type_text
    )


def other_help(request):
    return help_view(
        request,
        'help_pages/other.html',
        OtherForm,
        'OTHER',
        lambda answer: answer['other_need']
    )


def travel_help(request):
    return help_view(
        request,
        'help_pages/travel.html',
        TravelForm,
        'TRAVEL',
        lambda answer: answer['travel_need']
    )


def phone_help(request):
    return help_view(
        request,
        'help_pages/phone.html',
        PhoneHelpForm,
        'PHONE_HEL',
        lambda answer: ''
    )


def workers_help(request):
    def generate_type_text(answer):
        return f'שם מוסד העבודה: {answer["workplace_name"]}\n{answer["workplace_need"]}'

    return help_view(
        request,
        'help_pages/workers.html',
        WorkersForm,
        'VITAL_WORK',
        generate_type_text
    )
