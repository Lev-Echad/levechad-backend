from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import *
from .models import Volunteer, City, Language, VolunteerSchedule, HelpRequest, Area


def thanks(request):
    return render(request, 'thanks.html', {})


def homepage(request):
    return render(request, 'index.html', {})


def donation(request):
    return render(request, 'donation.html', {})


def get_help(request):
    return render(request, 'get_help.html', {})


def volunteer(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data
            languagesGot = Language.objects.filter(name__in=answer["languages"])
            areasGot = Area.objects.filter(name__in=answer["area"])
            volunter_new = Volunteer(tz_number = answer["identity"], full_name=answer["full_name"], age=answer["age"],
                                     phone_number=answer["phone_number"],
                                     city=City.objects.get(name=answer["city"]), address=answer["address"],
                                     available_saturday=answer["available_on_saturday"],
                                     notes=answer["notes"], moving_way=answer["transportation"],
                                     hearing_way=answer["hearing_way"], guiding=answer["want_guide"], keep_mandatory_worker_children = answer["childrens"])
            volunter_new.save()
            volunter_new.languages.set(languagesGot)
            volunter_new.areas.set(areasGot)
            volunter_new.save()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:y
            return HttpResponseRedirect('/client/schedule?vol_id=' + str(volunter_new.pk))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = VolunteerForm()

    return render(request, 'volunteer.html', {'form': form})


def schedule(request):

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            answer = form.cleaned_data
            new_schedule = VolunteerSchedule(Sunday="".join(answer["sunday"]), Monday="".join(answer["monday"]),
                                             Tuesday="".join(answer["tuesday"]), Wednesday="".join(answer["wednesday"]),
                                             Thursday="".join(answer["thursday"]), Friday="".join(answer["friday"]),
                                             Saturday="".join(answer["saturday"]), end_date=answer["end_date"])
            volunteerSchedule = Volunteer.objects.get(id=int(request.POST.get('vol_id', '')))
            new_schedule.save()
            volunteerSchedule.schedule = new_schedule
            volunteerSchedule.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            return HttpResponseRedirect('/client/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ScheduleForm()

    return render(request, 'schedule.html', {'form': form, 'id':request.GET.get('vol_id', '')})


def shopping_help(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ShoppingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            answer = form.cleaned_data
            new_request = HelpRequest(full_name = answer["full_name"], phone_number = answer["phone_number"], city = City.objects.get(name=answer["city"]),
                                      address = answer["address"], notes = answer["notes"], type = "BUYIN", type_text = answer["to_buy"])
            new_request.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:y
            return HttpResponseRedirect('/client/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ShoppingForm()

    return render(request, 'help_pages/shopping.html', {'form': form})


def medic_help(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MedicForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            answer = form.cleaned_data
            type_text = ""
            if(answer["need_prescription"]):
                type_text = "\nתרופת מרשם"
            new_request = HelpRequest(full_name = answer["full_name"], phone_number = answer["phone_number"], city = City.objects.get(name=answer["city"]),
                                      address = answer["address"], notes = answer["notes"], type = "MEDICI", type_text = type_text + answer["medic_name"])
            new_request.save()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:y
            return HttpResponseRedirect('/client/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MedicForm()

    return render(request, 'help_pages/medic.html', {'form': form})


def other_help(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = OtherForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            answer = form.cleaned_data
            new_request = HelpRequest(full_name = answer["full_name"], phone_number = answer["phone_number"], city = City.objects.get(name=answer["city"]),
                                      address = answer["address"], notes = answer["notes"], type = "OTHER", type_text = answer["other_need"])
            new_request.save()
            return HttpResponseRedirect('/client/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = OtherForm()

    return render(request, 'help_pages/other.html', {'form': form})


def home_help(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HomeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            answer = form.cleaned_data
            new_request = HelpRequest(full_name = answer["full_name"], phone_number = answer["phone_number"], city = City.objects.get(name=answer["city"]),
                                      address = answer["address"], notes = answer["notes"], type = "HOME_HEL", type_text = answer["need_text"])
            new_request.save()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:y
            return HttpResponseRedirect('/client/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = HomeForm()

    return render(request, 'help_pages/home.html', {'form': form})


def travel_help(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TravelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            answer = form.cleaned_data
            new_request = HelpRequest(full_name = answer["full_name"], phone_number = answer["phone_number"], city = City.objects.get(name=answer["city"]),
                                      address = answer["address"], notes = answer["notes"], type = "TRAVEL", type_text = answer["travel_need"])
            new_request.save()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:y
            return HttpResponseRedirect('/client/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TravelForm()

    return render(request, 'help_pages/travel.html', {'form': form})


def phone_help(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BaseHelpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            answer = form.cleaned_data
            new_request = HelpRequest(full_name = answer["full_name"], phone_number = answer["phone_number"], city = City.objects.get(name=answer["city"]),
                                      address = answer["address"], notes = answer["notes"], type = "PHONE_HEL", type_text = "")
            new_request.save()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:y
            return HttpResponseRedirect('/client/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BaseHelpForm()

    return render(request, 'help_pages/phone.html', {'form': form})

def helper_help(pk, fullName):
    return HelpRequest.objects.get(pk = pk, full_name = fullName)
