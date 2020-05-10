from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from .forms import *
from .models import Volunteer, City, Language, VolunteerSchedule, VolunteerCertificate, HelpRequest, Area
from django.db.models.functions import Concat
from django.db.models import Value, CharField, F

from urllib.parse import urljoin


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
    return redirect(settings.FRONTEND_BASE_URI)


def get_help(request):
    return redirect(urljoin(settings.FRONTEND_BASE_URI, "citizen/"))


def volunteer_view(request):
    return redirect(urljoin(settings.FRONTEND_BASE_URI, "volunteer/signup"))


def schedule(request):
    """
    View is kept only to redirect people who somehow stayed on this page or were redirected,
    and should be removed in future versions.
    :param request:
    :return:
    """
    return redirect(urljoin(settings.FRONTEND_BASE_URI, "volunteer/signup"))


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
    return redirect(urljoin(settings.FRONTEND_BASE_URI, "citizen/"))


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
