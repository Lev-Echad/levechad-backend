from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm, VolunteerForm, ScheduleForm, HelpForm, BuyInForm, MediciForm, HomeHelpForm, OtherForm


def volunteer(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VolunteerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:y
            return HttpResponseRedirect('/client/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VolunteerForm()

    return render(request, 'volunteer.html', {'form': form})


def schedule(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ScheduleForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/client/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ScheduleForm()

    return render(request, 'schedule.html', {'form': form})


def first_help(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HelpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            type = form.cleaned_data['type']
            if(type == 'BUYIN'):
                return HttpResponseRedirect('/client/buy_in')
            elif(type == "MEDICI"):
                return HttpResponseRedirect('/client/medic')
            elif(type == "HOME_HEL"):
                return HttpResponseRedirect('/client/homehelp')
            elif(type == "PHONE_HEL"):
                return HttpResponseRedirect('/client/phonehelp')
            elif(type == "OTHER"):
                return HttpResponseRedirect('/client/otherhelp')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = HelpForm()

    return render(request, 'help.html', {'form': form})


def buy_in(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BuyInForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/client/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BuyInForm()

    return render(request, 'buyin.html', {'form': form})


def medic(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MediciForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/client/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MediciForm()

    return render(request, 'medici.html', {'form': form})


def home_help(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HomeHelpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/client/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = HomeHelpForm()

    return render(request, 'homehelp.html', {'form': form})


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BuyInForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/client/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BuyInForm()

    return render(request, 'volunteer.html', {'form': form})


def thanks(request):
    return render(request, 'thanks.html', {})

def homepage(request):
    return render(request, 'index.html', {})
