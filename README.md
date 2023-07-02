# Applo AppStore

### Description & Problem Statement

Problem was to make Appstore clone where Admin can add Android Apps and Users can download the apps added by admin 
and earn points.

This app is based on REST API built using Django and DjangoRestFramework which support basic CRUD Operations and 
helped by GUI built on React.Js

Tech Stack:
```
Python
Django
Django Rest-framework
Postgres
Simple-JWT
Swagger
React.js
```

In this current version of the project, I have added Admin and User entities, for which multiple APIs 
are built to perform tasks like CRUD Operations, Adding Application, Updating Application, User registration, 
Downloading app, viewing 
apps, completing downloading task, and profile management respectively.

Alongside the user APIs, the `login` and `logout` APIs are also available in addition to the user APIs to obtain 
authorization tokens.

Regarding `Authorization` and `permissions`, I have used `Bearer` & `JWT` to validate user request and certain 
permissions classes of rest_framework are used to authorize the request.

---

### Prerequisties
To run this project on a machine, we need `Python` and `Postgres` database as basic requirements.

#### Install Steps
- First and foremost, start by creating a virtual environment the current directory. I have used `virtual` as the name 
  of the virtual environment.
```python
python -m venv virtual
```
- Once done with the installation, navigate to the virtual environment and activate it(below is for linux).
```shell
source virtual/bin/activate
```
- Now install all the dependencies using pip and `requirement.txt` file.
```python
pip install -r requirement.txt
```

Now that dependencies are ready, proceed to set up the project.

### Setup & Intitial Steps

- Create a django-project using `django-admin`, post that you will get to see some  configuration files
```shell
django-admin startproject applo
```
- Change directory to `applo` and start your new app(perform this to create any new app)
```shell
django-admin statapp mod_apps
```

- This project uses `.env` file to store all our secret keys, so create a `.env` file and store following variables. 
  Make sure to connect `.env` file to settings.py. Google it!!
```.dotenv
DB_NAME={your database name}
DB_USER={your database user's name}
DB_PASSWORD={your database user's password}
DB_HOST=127.0.0.1 or {url of database if using remote databse}
DB_PORT=5432
```

- As we are using DjangoRestFramework, make sure to add `'rest_framework'` in INSTALLED_APPS in settings.py of your 
  project. `drf-yasg` is used for using swagger, do add it to.
```python
INSTALLED_APPS = [
    'drf_yasg',
    'rest_framework',
]
```

- After this is done, we migrate our model
```shell
python3 manage.py migrate
```

- Now that migration is done, we are ready to run our application

```shell
python3 manage.py runserver
```

- You can create a superuser/admin user and provide all the details required afterwards
```shell
./manage.py createsuperuser 
```
---

### Usage


- The resources/Endpoints provided in this project are as follows: 









