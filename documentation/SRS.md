# EDU Flask App

# 1. Project description
EDU Flask App is the web application with user authentication and course management system.

The app should provide the following functionality:
- Registering, authorizing and saving users to the db
- Once registered user have to confirm their registration by going through 
email validation procedure. Otherwise their access to the app is limited.
- Creating, editing and deleting courses by users and saving it to the db
- View all courses present with info about them (name, short description, 
difficulty level, exam option, author name, date created and date updated)
- Search for (filter) courses by author, date created period, exam option 
and difficulty level (supports search on several criteria).
- User can enroll to and unenroll from a course
- User can view all courses he/she has created and enrolled to and number 
of users enrolled to it in the dashboard
- Author of the course may expell a user
- Have an API service thas supports common CRUD operations on users and 
courses (see Use cases below for more details)

## 1.1. Purpose
This application was developed as a final project for **EPAM Autumn 2021 
Python** School Course. Participants could choose any topic they wish though 
the project should comply to the technical requirements (use the following 
technologies):
- flask
- sqalchemy
- db (any -> PostgreSQL)
- pylint
- gunicorn
- travis CI
- coveralls
- unit tests (unittest or **pytest**)

## 1.2. Success criteria
The project should meet the following criteria:
- Web application has been deployed and runs on local instance
- Web application uses web service to fetch the data from database
- Be able to explain the chain of calls, starting from a browser to db, 
going through web layers
- Unit tests created
- Debug information is displayed at the debugging level in the console 
and in  a separate file
- Classes and functions / methods have docstrings comments
- Gunicorn configured properly
- README contains a brief description of the project, instructions on how 
to build a project from the command line, how to start it, and at what 
addresses the Web service and the Web application will be available after 
launch - Create pull request(s) in GitHub.
- Travis-CI build was successfull after merging the pull request(s)


# 2. Components

## 2.1. Users

### 2.1.1. Authentification and registration of users

#### 2.1.1.1. Registration

The app has signup route that renders signup page with the form for user 
registration. 

***Main scenario:***
- User follows the 'Sign Up' link in the navbar
- User fills the provided fields
- User submits the data by clicking the 'Sign Up' button 

The form includes five fields: 
- email - valid and unique email account name
- username - unique username
- password - password 
- password repeat - password repeat
- sign up - submit button

![sign up form](/documentation/images/signup.png)
*Pic. 1.1. Sign up form*

It has some built-in WTForms validators and custom ones. Displays validation 
errors within the form.

Validators:
- fields cannot be empty
- email - valied email account that is not taken by another user and with max 
lenght = 64
- username - username with lenght from 3 to 64 chars that is not taken by 
another user. Only letters, numbers, dots or underscores.
- password - the length of password should be minimum 6 and maximum 32 chars

![sign up form validation](/documentation/images/signup_validation.png)
*Pic. 1.2. Sign up form with validators raised*

Having submitted a signup form the user is redirected to login page with
a blue dismissable pop-up notification at the top of the page with a message 
that a confirmation letter with a token was sent.

![log in page with confirmation letter sent](/documentation/images/confirmation_sent.png)
*Pic. 1.3. Log in page with a pop-up message*


#### 2.1.1.2. Authentification

##### 2.1.1.2.1. Loggin in

The app has the login route that renders login page with the form for user
authentification.

***Main scenario***
- User follows the 'Log In' link in the navbar
- User fills the provided fields
- User submits the data by clicking the 'Log In' button
- If the user is not registered, he/she may follwo the signup link

The form includes four fields: 
- email - valid email account name user for signing up
- password - password 
- log in - submit button
- remember me - radio button to keep the user logged in 

![login in form](/documentation/images/login.png)
*Pic. 2.1. Login form*

It has some built-in WTForms validators and custom ones. Displays validation 
errors within the form. 

Validation:
- fields cannot be empty
- email - valid email address user for signing up
- password - password provided by the user in signup form
- email and password should match

In case the email or password are invalid displays the red dismissable pop-up
notification with error message.

![login in form](/documentation/images/login_invalid.png)
*Pic. 2.2. Login form invalid credentials error raised*

Having provided the valid credentials and submitted the login form the user is 
redirected to the dashboard page with a green dismissable pop-up notification
with message that user has logged in.

![dashboard page](/documentation/images/dashboard_new_user.png)


##### 2.1.1.2.1. Loggin out

The app has the logout route that logs out the user and redirects to the 
landing page.

***Main scenario***
- User follows the 'Log out' link in the navbar
- User is redirected to 'Landing Page'

Having followed the 'Log out' link the green dismissable pop-up window at the
top of the page is displayed with message of user's successfull logging out

![landing page after log out](/documentation/images/logout.png)


#### 2.1.1.3. Confirmation of a user registration

Having clicked the link in the message sent to the email account provided by 
user in the sign up form, the user is redirected to the login page with the 
red dismissable pop-up notification at the top of the page with a message that
the should log in to complete the registration.

![log in page with confirmed account](/documentation/images/confirmation_login.png)

Having logged in the user is redirected to the landing page with two green 
dismissable pop-up notifications with confirming the user registration and
informing that the user has logge in.

![landing page with logged in and confirmed account](/documentation/images/landing_confirmation_success.png)





