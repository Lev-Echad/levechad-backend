LevEchad
===========

A system to rule the volunteers and help requests of the LevEchad organization.

[levechad.org](http://levechad.org)

How to use
-----------

To run the server, use the following function:

    pip install -r requirements.txt
    python manage.py collectstatic
    python manage.py runserver

To add admin user and see the databases:

    python manage.py createsuperuser

And then log into the <http://localhost:8000/admin> and you will be able to see the databases.

How to update models
------------
To update the models, run ```git pull``` and then run the following:

    python manage.py makemigrations client
    python manage.py migrate client

Contributing
------------
The repository is open source and any contribution is appreciated !
you can add code by forking the repository, commit some code and create a pull request to 'develop' branch.
If you need a direct permission for branch creating / commits you can request that by creating an issue.
