LevEchad
===========

*Join us on Gitter:* [![Gitter](https://badges.gitter.im/LevEchadTech/community.svg)](https://gitter.im/LevEchadTech/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

This is a python 3 web application in the Django framework. 

The application manages the  LevEchad volunteers and provides an interface for submitting help requests to the organization. 

Further information about LevEchad can be found in this link:

[levechad.org](http://levechad.org)

First time setup
-----------

If this is the firsts time you're running this app, several set up steps are required to get your environment ready.

It is recommended that you perform these steps within a python virtual environment, otherwise the makeup of your python 3 installation might change:

    # On Windows:
    pip install virtualenv virtualenvwrapper-win
    mkvirtualenv levechad
    # The prompt should now be prefixed with (levechad) - this way you know you're on the Virtual Environment.
    # To deactivate:
    deactivate
    # To work on the virtual environment again:
    workon levechad

Before performing the listed steps make sure that the version of python you get when you type the python command into your terminal is the correct one!


As a first time setup, cd to the root folder of this project (should be name LevEchad) and perform the following steps:

	pip install -r requirements.txt
	python manage.py collectstatic
	python manage.py migrate
	python setup.py
	python manage.py runserver

To add admin user and see the databases:

    python manage.py createsuperuser

And then log into the <http://localhost:8000/admin> and you will be able to see the databases.

Pulling issues
-----------
When you pull an issue, you need to make sure your local repository is up to date with the latest changes in the code.

If you forked from the main repository into one of your own in the past, please follow these instructions:

[updating forked repository](https://medium.com/@topspinj/how-to-git-rebase-into-a-forked-repo-c9f05e821c8a)

If you are working within the main repository, type the following into git bash:

	git checkout develop
	git pull
	git checkout -b bugfix#

where # is the number of the github issue you wish to solve. 


Regardless of the repository you use, you need to make sure that the local SQLite DB is up to date with the ORM model in your updated code.

For this, run the following commands:

    python manage.py migrate
	

Contributing
------------
The repository is open source and any contribution is appreciated !

If  any part of this guide seems not to work no your machine, you are welcome to open an issue on the subject to receive help and resolve the problem.
