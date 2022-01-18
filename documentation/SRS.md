# EDU Flask App

---

## Table of contents:

1. [Project description](#1.-project-description)
    1. [Purpose](#1.1.-purpose)
    2. [Success criteria](#1.2.-success-criteria)
2. [Components](#2.-components)
    1. [Users](#2.1.-users)
        1. [Registration and authentification](#2.1.1.-registration-and-authentification)
            1. [Registration](#2.1.1.1.-registration)
            2. [Authentification](#2.1.1.2.-authentification)
                1. [Log in](#2.1.1.2.1.-log-in)
                2. [Log out](#2.1.1.2.2.-log-out)
            3. [Confirmation of registration](#2.1.1.3.-confirmation-of-registration)
    2. [Courses](#2.2.-courses)
        1. [Courses page](#2.2.1.-courses-page)
            1. [Display the list of courses](#2.2.1.1.-display-the-list-of-courses)
            2. [Add courses](#2.2.1.2.-add-courses)
            3. [Enroll to a course](#2.2.1.3.-enroll-to-a-course)
            4. [Unenroll from a course](#2.2.1.4.-unenroll-from-a-course)
        2. [Dashboard page](#2.2.2.-dashboard-page)
            1. [Display the list of courses](#2.2.2.1.-display-the-list-of-courses)
            2. [Add courses](#2.2.2.2.-add-courses)
            3. [Edit courses](#2.2.2.3.-edit-courses)
            4. [Remove courses](#2.2.2.4-remove-courses)
            5. [Unenroll from a course](#2.2.2.5.-unenroll-from-a-course)
        3. [Course page](#2.2.3.-course-page)
            1. [Enroll to a course](#2.2.3.1.-enroll-to-a-course)
            2. [Unenroll from a course](#2.2.3.2.-unenroll-from-a-course)
            3. [Expell user](#2.2.3.3.-expell-user)

---


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

### 2.1.1. Registration and authentification

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
*Pic. 1. Sign up form*

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

*Pic. 2. Sign up form with validators raised*

Having submitted a signup form the user is redirected to login page with
a blue dismissable pop-up notification at the top of the page with a message 
that a confirmation letter with a token was sent.

![log in page with confirmation letter sent](/documentation/images/confirmation_sent.png)
*Pic. 3. Log in page with a pop-up message*


#### 2.1.1.2. Authentification

##### 2.1.1.2.1. Log in

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
*Pic. 4. Login form*

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
*Pic. 5. Login form invalid credentials error raised*

Having provided the valid credentials and submitted the login form the user is 
redirected to the dashboard page with a green dismissable pop-up notification
with message that user has logged in.

![dashboard page](/documentation/images/login_dashboard.png)
*Pic. 6. Dashboard page. Successfull login*


##### 2.1.1.2.2. Log out

The app has the logout route that logs out the user and redirects to the 
landing page.

***Main scenario:***
- User follows the 'Log out' link in the navbar
- User is redirected to 'Landing Page'

Having followed the 'Log out' link the green dismissable pop-up window at the
top of the page is displayed with message of user's successfull logging out

![landing page after log out](/documentation/images/logout.png)
*Pic. 7. Landing page. Successfull log out*


#### 2.1.1.3. Confirmation of registration

Having clicked the link in the message sent to the email account provided by 
user in the sign up form, the user is redirected to the login page with the 
red dismissable pop-up notification at the top of the page with a message that
the should log in to complete the registration.

![log in page with confirmed account](/documentation/images/confirmation_login.png)
*Pic. 8. Login page after following confirmation link*

Having logged in the user is redirected to the landing page with two green 
dismissable pop-up notifications with confirming the user registration and
informing that the user has logge in.

![landing page with logged in and confirmed account](/documentation/images/landing_confirmation_success.png)
*Pic. 9. Landing page. Successfull login and confirmation*

In case the user logs in without confirming his/her account, the access to the
certain routes of the app is restricted.

![restricted access, not confirmed](/documentation/images/not_confirmed.png)
*Pic. 10. Landing page. Successfull login and confirmation*

In case the confirmation link has expired it is possible to ask for a new one
by following the instructions on the restricted page. The blue pop-up message
will show up.

![landing page. new confirmation code](/documentation/images/new_confirm_message.png)
*Pic. 11. New confirmation code sent*


## 2.2. Courses

### 2.2.1. Courses page

The page is designed to the display the list of all availiable courses. 
It includes the 'Manage courses' panel with the help of which users can
filter courses using diffenrent criteria as well as adding new courses.
The content of 'Manage courses' changes depending on whether the user is
logged in and confirmed the registration.

#### 2.2.1.1. Display the list of courses

***Main scenario:***
- User navigates to 'Courses' page
- Application displays the list of courses with pagination at the bottom 
(max 8 courses per page)
- Courses are displayes in the descending order based on the date created field
- 'Courses' page include two buttons ('Course Search' and 'Add New Course' 
if a user is logged in) at the 'Manage courses' panel at the top of the page
- Each course displayed includes information about it and a button at the 
bottom of the 'course' window
- User clicks 'Course search' button within the 'Manage courses' window
to filter courses after which the user is redirected to search page with
a search form.

![courses page, anonymous user](/documentation/images/courses_not_auth.png)
*Pic. 12. Courses page of anonymous user*

![courses page, logged in user](/documentation/images/courses_auth.png)
*Pic. 13. Courses page of logged in user*

![courses page, pagination](/documentation/images/courses_pagination.png)
*Pic. 14. Courses page - pagination*

The 'Courses page' consists of courses which displays the following info:
- Course name
- Author's name
- Short description of the course
- Difficulty level - I, R, or A
- Created on - date course created (format %d%M%Y)
- last updated on - date course last updated (format %d%M%Y)

***Filtering courses:***
- Having clicked the 'Search courses' button the user is redirected to the
'Find Courses' page with a form to apply filters
- Having applied the filters the user clicks the 'Filter courses' button and
is redirected to 'Courses Page' with the list of courses displayed
- The user may apply several filters including date range

!['Search form'](/documentation/images/find_course.png)
*Pic. 15. Find courses page with a search form*

The following filters could be applied:
- Author name - course which author's name is. In case no user exists with the
name provided, the pop-up message at the top of the page is displayed.
- Created from - date field (starting date)
- Created to - date field (end date)
- Exam? - select field with three options: 
    - All courses
    - With exam
    - No exam
- Difficulty level - select field with four options: 
    - All levels
    - Introductory
    - Regular
    - Advanced

Having applied the filters and clicked the 'Filter Courses' button the user is
redirected to courses/search route with filtered courses displayed. The either
green or red pop-up window is displayed signaling either that 1) the courses 
have been found or 2) a) user with that name does not exist (if applied), 
b) no courses found.

!['Search result page: Success'](/documentation/images/course_found.png)
*Pic. 16. Found 6 courses*

!['Search result page: user do not exist'](/documentation/images/course_user_not_found.png)
*Pic. 17. User does not exist*

!['Search result page: No courses found'](/documentation/images/course_found_not.png)
*Pic. 18. No courses found*


#### 2.2.1.2. Add courses

***Main scenario:***
- Users clicks the 'Add New Course' button
- Application redirects user to 'Create new course' page and displays a form
- User fills the fields and click 'Create Course' button
- If data is entered incorrectly, notifications are displayed
- If entered data is correct the record is added to the db
- If new course record is successfully added, then the user is redirected to
the 'Courses page' with the list of courses displayed

Create new course form consists of the following fields:
- Course label - course name (from 3 to 64 chars)
- Course description - short course description (from 3 to 250 chars)
- Exam? - radio button when clicked signals that the course includes exam
- Difficulty level - select field with three options:
    - Introductory
    - Regular
    - Advanced
- Create Course - button to create course and proceed to the 'Courses' page

!['Create course page with a form](/documentation/images/create_course.png)
*Pic. 19. Create course page with a form*

Validators:
- 'Course label' and 'Course description' fields cannot be empty
- The data provided to 'Course label' field should be unique and have from
3 to 64 chars max
- The data provided to 'Course description' field should have at least 3 and 
250 chars max

!['Create course form raises errors](/documentation/images/create_course_invalid.png)
*Pic. 19. Create course page with a form*

Having submitted a create course form the user is redirected to the newly 
created course page with a green dismissable pop-up notification at the top 
of the page with a message that the course has been created successfully.

!['Newly created course page](/documentation/images/course_page_created.png)
*Pic. 20. Newly created course page*

#### 2.2.1.3. Enroll to a course

***Main scenario:***
- User clicks the red 'Enroll right now!' button within the course he/she
he/she wants to enroll
- Application redirects the user to the 'Dashboard' page which displays the
list of courses with the course added to the 'Courses you are enrolled in'
section
- Green pop-up messages shows up at the top of the 'Dashboard' page marking
the successfull enrollment

!['Dashboard after course unenrollment'](/documentation/images/enroll_success.png)
*Pic. 21. Dashboard after course unenrollment*

#### 2.2.1.4. Unenroll from a course

***Main scenario:***
- User clicks the red 'Unenroll' button within the course course he/she wants 
to leave
- - Application redirects the user to the 'Dashboard' page which displays the
list of courses with the course removed from the 'Courses you are enrolled in' section
- Green pop-up messages shows up at the top of the 'Dashboard' page marking
the successfull unenrollment

!['Dashboard after course unenrollment'](/documentation/images/dashboard_after_delete.png)
*Pic. 22. Dashboard after course unenrollment*

### 2.2.2. Dashboard page

The 'Dashboard' page is divided into main sections: 1) 'Courses you created' 
and 2) 'Courses you are enrolled in'. The first section displays the list 
of the courses the user has created so far with a buttons to edit and delete
a course. The second section that displays the courses the user has enrolled 
in in the same manner as in the first section but with 'Unenroll' button to
manage courses. The page also has a windows where both the user name and the 
'Create course' button are displayed. 

!['Dashboard page'](/documentation/images/dashboard.png)
*Pic. 23. Dashboard page*


#### 2.2.2.1. Display the list of courses

***Main scenario:***
- user clicks the 'Dashboard' link at the navbar
- application displays the list of courses the user has created as well as
courses the user has enrolled

The newly created user or user that has not created nor enrolled to any 
courses expects to see the following dashboard page.

!['Blank Dashboard page'](/documentation/images/dashboard_new_user.png)
*Pic. 24. Blank dashboard page*

**The dashboard displays Courses in two sections:**
1. 'Courses you created' - courses created by the user
2. 'Courses you are enrolled in' - courses the user enrolled

**The first section diplays the courses with the following info:**
- '#' - the row number
- Label - the course name (label)
- Level - the course level (I, R, A)
- Exam - whether the exam is required (either True or False)
- Users - number of users enrolled to the course
- Created - date the course was created (format: %d%M%Y)
- Last updated - date the course was last updated (format: %d%M%Y)
- Handle - column with 'pencil' (edit) and 'trash' (delete) buttons

**The second section diplays the courses with the following info:**
- '#' - the row number
- Label - the course name (label)
- Level - the course level (I, R, A)
- Exam - whether the exam is required (either True or False)
- Handle - column with the 'Unenroll' button to leave the course


#### 2.2.2.2. Add courses

***Main scenario:*** *Same as in the 2.2.1.1. section.*


#### 2.2.2.3. Edit courses

***Main scenario:***
- User clicks the yellow button with the 'pencil' image in front of the course
he/she wants to edit
- User is redirected to edit course page with the edit form
- User edits the data and clicks the 'Save Course' button
- If data is entered incorrectly, error messages are displayed
- If entered data is correct the record is added to the db
- If new course record is successfully added, then the user is redirected to
the 'edited course' page.

!['Edit Course page'](/documentation/images/edit_course.png)
*Pic. 25. Edit Course page*

Edit course form consists of the following fields:
- Course label - course name (from 3 to 64 chars)
- Course description - short course description (from 3 to 250 chars)
- Exam? - radio button when clicked signals that the course includes exam
- Difficulty level - select field with three options:
    - Introductory
    - Regular
    - Advanced
- Save Course - button to create course and proceed to the 'Courses' page

Validators:
- 'Course label' and 'Course description' fields cannot be empty
- The data provided to 'Course label' field should be unique and have from
3 to 64 chars max. However, the course name may stay the same, it wont
trigger a conflict.
- The data provided to 'Course description' field should have at least 3 and 
250 chars max.

!['Edit Course page'](/documentation/images/edit_course_invalid.png)
*Pic. 26. Edit Course page*


#### 2.2.2.4. Remove courses

***Main scenario:***
- User clicks the red button with the 'trash' image in front of the course
he/she wants to delete
- Application displays confirmation dialog 'Delete <course_name> ?'
- User confirms the removal of the course
- Record is removed from the db
- The 'Dashboard' is displayed with a list of courses and the pop-up message 
at the top of the page confirming successfull deletion of the course

!['Delete modal window'](/documentation/images/delete_course.png)
*Pic. 27. Delete modal window*

!['Dashboard after course removal'](/documentation/images/dashboard_after_delete.png)
*Pic. 28. Dashboard after course removal*

***Cancel operation scenario:***
- User clicks the red button with the 'trash' image in front of the course
he/she wants to delete
- Application displays confirmation dialog 'Delete <course_name> ?'
- User clicks 'Cancel' button
- Dashboard with the list of created courses is displayed without changes


#### 2.2.2.5 Unenroll from a course

***Main scenario:***
- User clicks the red 'Unenroll' button in front of the course he/she wants 
to leave
- Application displays the list of courses with the course removed from the 
'Courses you are enrolled in' section
- Green pop-up messages shows up at the top of the 'Dashboard' page marking
the successfull unenrollment

!['Dashboard after course unenrollment'](/documentation/images/dashboard_after_delete.png)
*Pic. 29. Dashboard after course unenrollment*


### 2.2.3. Course page

The page represents the specific Course which displays basic info about course
as well as ability to both enroll to and uneroll from the course and in case
the user is the author of the course - to expell specific student.

!['Course page'](/documentation/images/course_page.png)
*Pic. 30. Course page with student enrolled*

#### 2.2.3.1. Enroll to a course

***Main scenario:***
- User clicks green 'Enroll' button
- User is redirected to the 'Dashboard' page which displays all the courses
where the course user enrolled to is added


#### 2.2.3.2. Unenroll from a course

***Main scenario:***
- User clicks red 'Unenroll' button
- User is redirected to the 'Dashboard' page which displays all the courses
where the course user unenrolled from is removed


#### 2.2.3.3. Expell user

***Main scenario:***
- User clicks the red 'Expell' button in front of the user he/she wants to
remove from the course.
- The user expelled is removed from the db
- The list of students is displayed with the user removed from the list
- In case the user who clicked the 'Expell' button is not the author of the
course the red pop-up windows shows-up at the top of the 'Course' page with 
an error message

!['Course page after the user is expelled'](/documentation/images/course_page_expelled.png)
*Pic. 31. Course page after the user is expelled*

!['Course page expell denied'](/documentation/images/course_page_expell_denied.png)
*Pic. 32. Course page with an error message*
