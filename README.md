# hemp-db

This repository will hosts all code and documentation for the Hemp DB Capstone, CS46X at Oregon State University

## Local Setup

1. Clone repository
2. `cp .env.example .env`
3. Add credentials to .env file
4. `docker build -t hempdb .`
5. `docker run --name hempdb-dev -it -p 8000:8000 -v $(pwd):/code hempdb`    `Note: If using powershell use {pwd} instead of (pwd)`
6. Open http://localhost:8000

## Local Development

1. Checkout new branch
2. `docker build -t hempdb .`
3. `docker run --name hempdb-dev -it -p 8000:8000 -v $(pwd):/code hempdb`     `Note: If using powershell use {pwd} instead of (pwd)`
Note:
* if container already exists, run `docker start -a hempdb-dev` 
5. Develop Features

**no need to restart docker, local code will be synced up with code in container. Just code, ctrl + s, see changes in browser**

6. Lint with `ruff check .`
6.a Fix with `ruff check . --fix`

7. Open PR

Make sure to add any new dependencies to requirements.txt

For migrations, run
1. `docker exec -it hempdb-dev bash`
2. `python manage.py makemigrations`
3. `python manage.py migrate`
