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
- First and foremost, start by creating a virtual environment the current directory. I have used `venv` as the name 
  of the virtual environment.
```python
python -m venv venv
```
- Once done with the installation, navigate to the virtual environment and activate it(below is for linux).
```shell
source venv/bin/activate
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

- You can create a superuser/admin user and provide all the details required afterwards. This superuser will server as an admin to add and manage android apps.
```shell
./manage.py createsuperuser 
```
---

### Usage

#### Endpoints

- The resources/Endpoints provided in this project are as follows: 
```
- /account/login/ - POST : for user/admin login, with username and password to get access token
- /account/user/register/ - POST : to create user
- /account/user/profile/ - GET : PATCH - to see user profile and to make changes.
- /account/logout/ - POST : for user/login, with refresh token

- /app/home/ - GET : shows all the apps on appstore, allows anyone
- /app/new/ - POST : allows only admin to add new app
- /app/admin/ - GET : allows any admin to list all the apps it added
- /app/admin/<int:pk>/ - GET,PATCH,DELETE : allows admin to see,update and delete any app it added.
- /app/category/add - POST : allows admin to add a unique category
- /app/category/list - GET : allows admin to get all unique category
- /app/subcategory/add/ - POST : allows admin to add a unique sub-category under any category
- /app/subcategory/list/ - GET : allows admin to get all unique sub-category under any category
- /app/user/<int:pk> - GET : allows user to see app details
- /app/user/download/<int:pk> - POST : allows user to download an app
- /app/user/download/list - GET : allows user to list the downloaded apps
- /app/user/task/list/ - GET : shows all the task for any specific user
- /app/user/task/<int:pk>/ - GET, PATCH : gives detail of any task and allows any user to add the screenshot and complete the task

- /swagger/ - to check for swagger documented APIs

```

- `/account/login/`, `/account/user/register/`, `/app/home/` do not require any authentication or authorisation, but all other endpoints requires authentication.
- Once we create a user, we can send a `POST` request to `/account/login/` to get `access` and `refresh` token for both admin and user.
- Now we can use this `access` token as `Bearer ${access}` as `Authorization` header in our request.
- Points earned by any user gets updated on `user_table` everytime user downloads any app adn can be retrieved easily

#### User-Interface

- for the UI part, 'login' and 'register' is only built based on 'React.js' . It takes username and password to login and for register it takes all the basic details required.

- login template was cloned from `https://github.com/Aatmjeet/React-JWT_login-template`



