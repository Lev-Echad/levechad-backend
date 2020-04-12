# LevEchad

Thank you for contributing to the LevEchad system! :fire:

To improve the code quality and consistency across the codebase, we have some guidelines that we
require our contributors to follow.


## Getting Started
See the [README](https://github.com/Lev-Echad/levechad-backend) file for more information on setting up the local
development environment (and [levechad-frontend's README](https://github.com/Lev-Echad/levechad-frontend) if you need
to set the frontend server up).


## Codebase Walkthrough
We currently have two repositories for this project: [levechad-frontend](https://github.com/Lev-Echad/levechad-frontend/)
and [levechad-backend](https://github.com/Lev-Echad/levechad-backend).

The backend system is currently going through a refactor, in which the `levechad-frontend` repository was created as
part of the effort to move the frontend to more modern technologies.

**The old system** consists of the _client_ and _server_ apps (at URLs /client and /server, respectively).

* The client app is the system for the users, containing help request views, volunteer forms, etc. and all of the models.
* The server app is only accessible to the LevEchad Hamal and all the view requires login, and is used to manage the
volunteers & help requests.

We currently only maintain the old system for bug-fixes (that may apply to both the new and old systems). Currently we
don't cleanup the Django frontend-related code (views, template) as it will be removed in the future in favor of the new
frontend.

**The new system** starts with the _api_ app, which serves the REST API using Django REST framework that the new
frontend can interface with. This also has temporary dependencies to the client app (because the models are there) until
the old system will be phased out completely.

Currently we support both systems, as the new system is currently being built and is still not in production.


## Fixing issues
* When looking for missions, you can choose from the [list of issues](https://github.com/Lev-Echad/levechad-backend/issues)
in our repo. It is also recommended to look at the [projects](https://github.com/Lev-Echad/levechad-backend/projects),
which are GitHub's Kanban Boards.
  * If you have an idea for an issue that's not listed, refer to the _Creating issues_ section of this document.
* Make sure to **assign yourself to the issue you're working on**, so two people won't work on the same thing by
accident.
* Branch from develop, and when you're finished, submit a PR (more on this below).

### Branching

* **We do not push to `develop` (the stable development branch) or `master` (the releases branch) directly - this only
happens through approved pull requests.**
* When creating an issue, make sure to branch from **`develop`**. Name your branch like so:

  ```bash
  issue/<issue-number>-<short-description>
  # For example, we could name the branch of issue #123 titled "Add S3 integration to volunteer certificate image caching":
  issue/123-cache-certificates-on-s3
  ``` 
* Create the branch on the original repo, don't fork - if you need permissions as a returning contributor, contact one
of the admins (including @astar26 and @stavlocker).
  * "Wandering contributors" that are not part of the contribution team can fork this repo and suggest changes as part
  of the open-sourced nature of the repo.
* Make as little commits as you can (preferably one before CR, and one for each CR cycle), and keep the titles concise.
* When finished, create a pull request (PR) to the `develop` branch. Remember to assign yourself to the PR. Also make
sure to link the issue to the PR.

### Fixing Pull Requests (Answering Code Reviews)
_After creating a PR, you must answer the code review (CR) given. There must be an approving reviewer on a PR to merge
it to the target branch._
* Make sure to address all the comments in your CR, by fixing them or commenting why you think they shouldn't be done.
* You will not be able to merge to the traget branch (usually `develop`) before you fix all the conflicts by merging
from the target branch to your branch. GitHub also shows if there are conflicts at the bottom of the pull request page.
* When your PR is merged/closed, make sure to close the original issue.

### Django migrations & dependencies
* When changing models in Django, you must run the Django command `makemigrations`, to create the migration files later
applied on the personal development DBs and the production DB. Use `migrate` to apply any unapplied migration files.

* When moving between branches, you want to keep your local database adjusted to the migrations you currently have. If
you're on a branch with new migrations and you want to switch branches, make sure to undo your migrations before
switching:

  ```
  python3 manage.py migrate client <base-migration-name>
  ```
  
  To install new python dependencies added to the project:
  
  ```
  pip install -r requirements.txt
  ```

#### Migration conflicts
Sometimes after submitting a PR with migrations, other migrations get merged into develop. When you will merge from
develop to you branch this will cause in two "leaf" migrations and running `migrate` will fail.
In order to fix this, revert to the base migration (the latest migration you created your migrations on top of), delete
the migration(s) you reverted, and re-migrate:

```
# Revert to base migration (<base-migration-name> is the name of the migration file without the extension):
python3 manage.py migrate client <base-migration-name>
# Delete the migrations reverted...
# Re-migrate:
python3 manage.py makemigrations
python3 manage.py migrate
```
More complicated conflicts may need special resolving, but the steps above are for the common case of conflicts.


## Coding Guidelines
* Make sure to use proper English throughout your code.
* Follow the PEP-8 conventions.
* Keep it DRY (Don't Repeat Yourself) - avoid code duplication. If you think a new module needs to be created for a
certain functionality, create it.
  * If this requires major cleanup/refactor on the old system side (see _Codebase Walkthrough_ above) you might want to
    reconsider. If you're unsure - just ask.
* If there are major changes to the current project structure you wish to make, it's best to talk to one of the admins
beforehand.
* Wherever you can, write text in English and use the [Django translation
system](https://docs.djangoproject.com/en/3.0/topics/i18n/translation/) (`gettext`) to translate to Hebrew (see #244
for backwards-changing).


## Creating issues
* Make sure to follow the issue template - make sure your issue isn't a duplicate and that it is clear & descriptive.
* Issues shouldn't be questions - if you have a question, feel free to ask in the contribution team's group, or one of
the admins.
