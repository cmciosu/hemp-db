# Developing on HempDB

## Local Setup

1. Clone repository
2. Set up .env
  * `cp .env.example .env`
  * Add credentials to .env file

3. Build the docker image
  * `docker build -t hempdb .`

4. Start Docker container
  * Mac/Linux: `docker run --name hempdb-dev -it -p 8000:8000 -v $(pwd):/code hempdb`    
  * Windows: `docker run --name hempdb-dev -it -p 8000:8000 -v ${pwd}:/code hempdb`
  * If container already exists: `docker start -a -i hempdb-dev`
  * To remove duplicate container: `docker rm hempdb-dev`

5. Open http://localhost:8000

## Local Development

1. Checkout new branch
  * `git checkout -b "<feature_name>"`

2. Develop feature
  * For migrations, run:
  * `docker exec -it hempdb-dev bash`
  * `python manage.py makemigrations`
  * `python manage.py migrate`
  * For new env vars, add to .env, .env.example, and vercel
  * Make sure to add any new dependencies to requirements.txt

3. Lint with ruff
  * Access the running container's shell with `docker exec -it hempdb-dev /bin/bash` in a new terminal
  * Lint with `ruff check .`
  * Fix any errors with `ruff check . --fix`

4. Open PR to dev

**Container does not need to be manually restarted with every code change, django uses StatReloader to auto-reload the code**

## Deploy to Production

1. Open PR dev -> main

### ⚠️⚠️⚠️ Make sure Debug is set to False ⚠️⚠️⚠️

1. Go to `hempdb/settings.py`, set Debug to False
2. Go to vercel, make sure build succeeded
3. Open PR to main