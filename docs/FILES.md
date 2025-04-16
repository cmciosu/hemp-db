# File Structure

This page outlines the file structure used for the HempDB project and is intended for developers and maintainers. 

```
hemp-db/
├─ .github/
├─ docs/
│  └─ images/
├─ hempdb/
└─ helloworld/
   ├─ management/
   │  └─ commands/
   ├─ migrations/
   └─ templates/
```
_A high-level folder structure of hemp-db._

## .github/
* Files related to GitHub Actions workflows and GitHub Issue templates.

## docs/
* Markdown files and images for this documentation site.

## hempdb/
* The Django "project" containing high-level configuration files like `settings.py` and the top-level `urls.py`.

## helloworld/
* The Django "app" containing a majority of the project's code. Notable folders/files include:
  * `migrations/`: files that track changes made to database schema. Documentation [here](https://docs.djangoproject.com/en/5.2/topics/migrations/).
  * `templates/`: files that construct the frontend interface using Django's templating syntax to dynamically insert content. Documentation [here](https://docs.djangoproject.com/en/5.2/topics/templates/).
  * `admin.py`: configuration for the Django admin portal. Documentation [here](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/).
  * `forms.py`: form definitions that are used on the frontend. Documentation [here](https://docs.djangoproject.com/en/5.2/ref/forms/api/).
  * `models.py`: database schema and table (model) definitions. Documentation [here](https://docs.djangoproject.com/en/5.2/topics/db/models/).
  * `signals.py`: code for Django's signal dispatcher to be run when certain events occur. Documentation [here](https://docs.djangoproject.com/en/5.2/topics/signals/).
  * `tests.py`: tests run on GitHub Actions. Documentation [here](https://docs.djangoproject.com/en/5.1/topics/testing/overview/).
  * `urls.py`: maps different URL paths corresponding views. Documentation [here](https://docs.djangoproject.com/en/5.2/topics/http/urls/).
  * `views.py`: handles HTTP requests by _typically_ querying the database, performing business logic, and responding with templates and corresponding data. Documentation [here](https://docs.djangoproject.com/en/5.1/topics/http/views/).
