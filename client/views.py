from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import *
from .models import Volunteer, City, Language, VolunteerSchedule, HelpRequest



# def schedule(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = ScheduleForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/client/thanks')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = ScheduleForm()
#
#     return render(request, 'schedule.html', {'form': form})
#
# def first_help(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = HelpForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             type = form.cleaned_data['type']
#             if(type == 'BUYIN'):
#                 return HttpResponseRedirect('/client/buy_in')
#             elif(type == "MEDICI"):
#                 return HttpResponseRedirect('/client/medic')
#             elif(type == "HOME_HEL"):
#                 return HttpResponseRedirect('/client/homehelp')
#             elif(type == "PHONE_HEL"):
#                 return HttpResponseRedirect('/client/thanks')
#             elif(type == "TRAVEL"):
#                 return HttpResponseRedirect('/client/thanks')
#             elif(type == "OTHER"):
#                 return HttpResponseRedirect('/client/otherhelp')
#
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = HelpForm()
#
#     return render(request, 'get_help.html', {'form': form})
#
# def buy_in(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = BuyInForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/client/thanks')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = BuyInForm()
#
#     return render(request, 'buyin.html', {'form': form})
#
#
# def medic(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = MediciForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/client/thanks')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = MediciForm()
#
#     return render(request, 'medici.html', {'form': form})
#
#
# def home_help(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = HomeHelpForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/client/thanks')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = HomeHelpForm()
#
#     return render(request, 'homehelp.html', {'form': form})


# ROYZ FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------


def thanks(request):
    return render(request, 'thanks.html', {})


def homepage(request):
    return render(request, 'index.html', {})


def donation(request):
    return render(request, 'donation.html', {})


def get_help(request):
    return render(request, 'get_help.html', {})


def send_help(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data
            volunter_new = Volunteer(full_name=answer["full_name"], age=answer["age"], area=answer["area"],
                                     languages=Language.objects.get(name=answer["languages"]),
                                     phone_number=answer["phone_number"],
                                     city=City.objects.get(name=answer["city"]), address=answer["address"],
                                     available_saturday=answer["available_on_saturday"],
                                     notes=answer["notes"], transportation=answer["transportation"],
                                     hearing_way=answer["hearing_way"])
            volunter_new.save()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:y
            return HttpResponseRedirect('/client/schedule?vol_id=' + volunter_new.pk)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = VolunteerForm()

    return render(request, 'send_help.html', {'form': form})


def schedule(request):

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            answer = form.cleaned_data
            new_schedule = VolunteerSchedule(sunday="".join(answer["sunday"]), monday="".join(answer["monday"]),
                                             tuesday="".join(answer["tuesday"]), wednesday="".join(answer["wednesday"]),
                                             thursday="".join(answer["thursday"]), friday="".join(answer["friday"]),
                                             saturday="".join(answer["saturday"]), end_date=answer["end_date"])
            volunteerSchedule = Volunteer.objects.get(id=request.GET.get('vol_id', ''))
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

    return render(request, 'schedule.html', {'form': form})


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
            return MedicForm('/client/thanks')

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

