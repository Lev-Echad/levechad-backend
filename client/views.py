from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import VolunteerForm, ScheduleForm, HelpForm

def volunteer(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VolunteerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/schedule/')

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
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ScheduleForm()

    return render(request, 'schedule.html', {'form': form})

def firstHelp(request):
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
                return HttpResponseRedirect('/buyin/')
            elif(type == "MEDICI"):
                return HttpResponseRedirect('/medic/')
            elif(type == "HOME_HEL"):
                return HttpResponseRedirect('/homehelp/')
            elif(type == "PHONE_HEL"):
                return HttpResponseRedirect('/phonehelp/')
            elif(type == "OTHER"):
                return HttpResponseRedirect('/otherhelp/')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = HelpForm()

    return render(request, 'help.html', {'form': form})

