# EDU Flask App

EDU App is the web application for creating educational courses as well as
enrolling to them.

It is a final project for EPAM Python Autumn 2021 Course. 
For more detailed information visit documentation/SRS.md

# How to start

## Download the project

- Run ```git clone https://github.com/AndrStp/flask_epam.git``` command in
your terminal to download the project files
- OR you may want to donwload project files using GitHub GUI.

## Set up local environment

- Navigate to the project root directory
- Run ```python3 -m venv venv``` OR ```python -m venv venv``` in case you are 
using Windows OS
- Run ```source venv/bin/activate``` to activate the virtual environment OR
run ```venv\Scripts\Activate.ps1``` in case of Windows OS

*For more info on creation and configuiring or virtual environment visit
https://docs.python.org/3/library/venv.html

## Install necessary dependencies
- Run ```python -m pip install -r requirements.txt```

*The project uses PostgreSQL db by default but you can use another db engine.
In this case you need to change the ***requirements.txt*** file to add the 
required dependencies.

## Configure

- Navigate to the project root directory
- Run ```mv .flaskenv.exmaple .env``` command to rename the .flaskenv.exmaple
file to .env
- Edit the .env by following the instuctions within the file.
- Optionally you may want to change the *app_config.py* to configure the app.
The file uses dotenv package to load the environment variables from .env file.
- Optionally ypu may want to change the *logging_config.py* to adjust logging.
By default uses *DEBUG* level and keeps logs in *logs/log.txt* file.

## Run
The project presumes using Docker to run the app but it's not neccessary as 
long you have another db server or using the sqlite db engine.

- ### Docker
    - Optionally Run ```docker built -t image_name``` to build an image 'image_name'
    - Run ```docker-compose up -d``` to run containers in the detached mode

- ### Without Docker
    - Reconfigure the app so that it may connect to the db
    - Run ```flask db init && flask db migrate && flask db upgrade``` to make
migrations
    - Run ```python run.py``` where *run.py* serves as entryponit

## Use

The app by default runs on the localhost, port 5000.

- ### Web Application:
```
/
/about
/courses
/courses/search (POST, GET)
/dashboard

/auth/signup
/auth/confirm
/auth/confirm/<token>
/auth/unconfirmed
/auth/login
/auth/logout

/enroll/<course_id>
/unenroll/<course_id>

/course/<course_id>
/course/create (POST, GET)
/course/delete/<course_id>
/course/edit/<course_id> (POST, GET)

/expell/<user_id>/from/<course_id>
/unenroll/<course_id>
/enroll/<course_id>
/static/<filename>
```

- ### Web Service:

```
/api/v1/users/ (GET)
/api/v1/users/<id>/ (GET, POST, DELETE, PUT)

/api/v1/courses/ (GET)
/api/v1/courses/<id>/' (GET, POST, DELETE, PUT)

/api/v1/courses/<course_id>/enroll/<user_id>/' (PUT)
/api/v1/courses/<course_id>/unenroll/<user_id>/' (PUT)
```
