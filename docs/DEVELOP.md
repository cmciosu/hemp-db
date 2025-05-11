# Developing on HempDB

This page details how to set up a local development environment and develop features. This page is intended for developers. Please read this entire page before developing on HempDB.

## Local Setup

1. Clone repository
2. Set up .env file
  * `cp .env.example .env`
  * Replace dummy values with actual values. Actual .env values and credentials can be obtained via Teams.

3. Build the docker image
  * `docker build -t hempdb .`

4. Start Docker container
  * Mac/Linux: `docker run --name hempdb-dev -it -p 8000:8000 -v $(pwd):/code hempdb`    
  * Windows (PowerShell): `docker run --name hempdb-dev -it -p 8000:8000 -v ${pwd}:/code hempdb`
  * If container already exists: `docker start -a -i hempdb-dev`
  * To remove duplicate container: `docker rm hempdb-dev`

5. Open http://localhost:8000

**Container does not need to be manually restarted with every code change. Django uses StatReloader to auto-reload the code**

## Local Development

1. Checkout new branch
  * `git checkout -b "<feature_name>"`

2. Develop feature
  * For features that alter database schema, make and run migrations with the following commands:
  * `docker exec -it hempdb-dev bash`
  * `python manage.py makemigrations`
  * `python manage.py migrate`
  * For features that add new env vars, add them to your .env, the .env.example, and to Vercel
  * Add any new dependencies to requirements.txt. You will need to rebuild your docker image when dependencies are added.

3. Lint with ruff
  * Access the running container's shell with `docker exec -it hempdb-dev bash` in a separate terminal
  * Lint with `ruff check .`
  * Fix any errors with `ruff check . --fix`

4. Push branch and open PR

### ⚠️⚠️⚠️ Before Pushing to GitHub, Ensure `DEBUG = False` ⚠️⚠️⚠️

To do this, go to `hempdb/settings.py` and set `DEBUG = False`

**Important:** The `DEBUG` flag is also used to configure things like whether emails are actually sent to people, or just logged to the console (see `settings.py`). As a result, please set `DEBUG = True` when you're developing locally.

* For example, if you edit a company locally, an email notification may get sent to non-developers, even if you're connected to the development database.
* This happens because of the nature of the development database. It was created by duplicating the production database, which contains information like users and if they are in an admin group (this is how the email system determines who to send emails to in `notifications.py`).
