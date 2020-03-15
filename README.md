LevEchad
===========

A system to rule the volunteers and help requests of the LevEchad organization.

[levechad.org](http://levechad.org)

How to use
-----------

To run the server, use the following function:

    pip install -r requirements.txt
    python manage.py runserver

To add admin user and see the databases:

    python manage.py createsuperuser

And then log into the <http://localhost:8000/admin> and you will be able to see the databases.

How to update models
------------
To update the models, run ```git pull``` and then run the following:

    python manage.py makemigrations client
    python manage.py migrate --fake-initial

