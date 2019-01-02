[![Build Status](https://travis-ci.org/mike2151/Online-OH-queue.svg?branch=master)](https://travis-ci.org/mike2151/Online-OH-queue) [![codecov](https://codecov.io/gh/mike2151/Online-OH-queue/branch/master/graph/badge.svg)](https://codecov.io/gh/mike2151/Online-OH-queue)

# Online Office Hours Queue
## About
Online-OH-Queue is a web app for hosting online office hours. Students have the ability to sign up with a question and TAs can view the order of students signed up and answer their questions in a first in first out basis. 
## Table of Contents 
[Features](#Features) 
<a name="Features"/> <br/>
[Setup](#Setup) 
<a name="Setup"/> <br/>
[Office Hours Queue Setup](#OHQueueSetUp) 
<a name="OHQueueSetUp"/> <br/>
[Admin Panel](#Admin-Panel) 
<a name="Admin-Panel"/> <br/>
[Teaching Assistants](#Teaching-Assistants) 
<a name="Teaching-Assistants"/> <br/>
[Pages](#Pages) 
<a name="Pages"/> <br/>
[Development](#Development) 
<a name="Development"/><br/>
[API](#API) 
<a name="API"/>


## Features
* Email verification
* Support for emails only in a school domain
* Real time updates to office hours queues
* Summaries for TAs preparing for their office hours
* Statistics
* Mobile and desktop displays
* DDOS protection


## Setup
### Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
<br />
To setup Online-OH-Queue, press the button above that will create a heroku application. Make sure you have a heroku account so you can make the website.

Upon clicking on the button, you will be prompted to enter information about the instance of Online-OH-Queue. Below are the highlighted areas of interest for setting up the office hours queue:


#### App Name
Enter the name of the heroku app. This will become your domain for the herokuapp. For example, if your app name is `cisohqueue`, then your website will be `cisohqueue.herokuapp.com`. 


#### Configuration Variables
These variables will make your instance of Online-OH-Queue unique to your course. You must enter information for each field. Enter reasonable values for each field. This web app is not prepared to handle ridiculous inputs to its configuration variables. Each field is described below:


##### COURSE_TITLE
This is the name of the corse. <br/>
Example: `CIS 121`

##### DOMAIN_NAME
This is the name of the website URL you will be running the website on. Include the full name as if you were entering it into a web browser. Exclude any http or https<br/>
Example: `cisohqueue.herokuapp.com` or `ohqueue.com`

##### EMAIL_HOST
This is the mame of the email host you will be using. Email hosting is important because password reset and account activation emails are all sent through an email host. The default value is the host for sendgrid.<br/>
Example: `smtp.sendgrid.net`

**NOTE**: If you choose to use sendgrid, which we recommend, once you create an account, navigate to [app.sendgrid.com/guide/integrate/langs/smtp](https://app.sendgrid.com/guide/integrate/langs/smtp) and you will see the fields `Server`, `Username`, and `Password` which all correspond to the three email configuration variables that you will have to set. 

##### EMAIL_USERNAME
Username for your email provider <br/>
Example: `apikey`

##### EMAIL_PASSWORD
Password for your email provider <br/>

##### PRIMARY_THEME_COLOR
By default, the Online-OH-Queue comes with a green color theme. This can be changed. This configuration variable represents the main color of the website. You must enter a valid hex color with the hashtag. If you do not want to deal with this, then leave it to the default value (the green). <br />
Example: `#76b852`

##### QUEUE_TIME_ZONE
This field tells the server which timezone it should operate in. The default value is `America/New_York` which represents New York time. A full list of all the timezones can be found here: [Time Zones](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568) <br/>
Example: `America/New_York`

##### SECRET_KEY
This is automatically generated so you do not need to worry about it.

##### START_OF_WEEK
This is the day of the week that starts the office hours weekly cycle. In other words, this value represents the day of the week when office hours start getting questions about a different homework or problem set. An example would be if homeworks were due on a weekly basis on Sunday, then Monday would be the start of the week with respect to office hours. <br/>
Example: `Monday`
<br />

#### Deploying the Application
When you enter everything, click `Deploy App`. Then click `Manage App` to do some additional set up.
<br />

#### Create the superuser
Each instance of the application needs to have a superuser or an admin to make other users admins and other users TAs. To create the first superuser, navigate to the drop down menu in the top right labeled `more`. Select the `run console` option and enter the following command: <br />
`python manage.py createsuperuser` <br />
You will then be prompted to enter the information for this account. The username can be whatever you want. Usually, it is a good idea to make it the same as your email. Once it says that the superuser was created successfully, you can exit the console window. **Do not lose this information**. 

#### Changing the Heroku Plan
You will likely need at least a hobby plan to be able to handle the traffic of your course. You can do so by going in the resources tab and clicking `Change Dyno Type` to `Hobby`. It will cost 7 dollars a month.

#### Changing the Site Name
We need to tell the server what domain we are using so it can properly send password reset and account confirmation emails. First, navigate to `/admin` and enter the credentials of the superuser you just created. <br />
Next, on the left hand side, click on `Sites`. Then, click on `example.com`. Change both fields to match what you put for the `DOMAIN_NAME` configuration variable from earlier. Finally, click `Save`

Next, you will need to set up Office Hours Queues. See the next section regarding that set up.



## OHQueueSetUp
Online-OH-Queue supports the creation of multiple queues. To create a queue, navigate to `/admin`, log in with the superuser credentials you created earlier or with another admin account.

Then, click on `+ Add` in the `OHQUEUE` section. <br />
Enter a name for the queue. This name will be visible to all students. <br />
Do not enter any questions. Ignore this field <br />
Do not enter the average wait time. Ignore this field. This will be automatically done by the server <br /><br />
Times Open Section: <br />
This field is used to specify when the queue is open for students to ask questions. You must enter a string in the following format: <br />
Example: `Monday:2:00pm-4:00pm;5:00pm-7:00pm Tuesday:11:30am-5:00pm Wednesday:11:30am-5:00pm Thursday:11:30am-5:00pm Friday:11:30am-5:00pm Saturday: Sunday: ` <br />
In the queue above, office hours are held 2pm to 4pm and 5pm to 7pm on Monday. On Tuesday to Friday, office hours are held  11:30 am to 5pm. There are no office hours held on Saturday or Sunday. <br />
Notes on the format: <br />
You must include **ALL** days of the week in the times open field. If there no office hours being held on that day, then leave a space after the colon. <br />
When specifying times, use the format above: hour:minuteam/pm. First indicate the hour. Next, a colon followed by the minutes. Next, either am or pm. The dash indicates a time range. So in the case of `2:00pm-4:00pm` the queue remains open from 2pm to 4pm. Simply typing `2pm-4pm` will crash the app. You must include the minutes.<br />
A semicolon followed by another time range is used if the queue is not open during a continuous time interval. See Monday for an example <br />
A space is followed after specifying a day of open times. <br />
**Failure to adhere to the time convention will make the Office Hours Queue not appear or may even bring up a failure error on the office hours page!**

Ignore all other fields.

## Admin-Panel
In `/admin` you can also do the following:
#### Make users TAs and Admins
To that, navigate to the `users` section. Select the user who you wish to be a TA. Click the checkbox that says `Teaching Assistant` then click save in the bottom right corner. 

To make a user an admin, you do the same process except check the `superuser_status` box.

**Note**: Admins have to make themselves TAs. Just because you are an Admin does not mean you are a TA by default.

## Teaching-Assistants
As a teaching assistant, you will have two main pages to visit: `/summary` and `/answer`. <br />
The summary page gives you all the questions asked in the weekly office hours cycle. You can use this to better prepare for office hours. <br />
The answer page allows you to view all the queues in the queues. Answer questions in the queue which means to remove students from the queue. Finally, you have the power to manually open and close queues. 

## Pages
This section describes each page and what it offers.

`/` <br />
The root directory is either a landing page for users to sign up or log in if the user is not authenticated. Or the page serves as a listing of available office hour queues if the user is authenticated.
<br />
`/login` <br />
Where the user logs in.
<br />

`/signup` <br />
Where the user makes an account
<br />

`/admin` <br />
Administrative portal. Only admins can see the portal. Here admins can create and manage office hours queues and change the permissions of users.
<br />

`/summary` <br />
This page will display all the questions asked in the office hours cycle week. If you are a TA, questions will appear. If you are not a TA, no questions will be populated.
<br />

`/<queuename>/ask` <br />
Ask a question for the given queue. Only authenticated users can do this. In addition, users can only ask one question at a time across all queues.
<br />

`/answer` <br />
This page is only visible to TAs. It allows you to view all queues in a queue and "answer" questions which will remove students from the queue. You also have the option to close and open queues manually. 
<br />


## Development
To develop and debug Online-OH-Queue, do the following steps:
1. Install Redis: [Redis install guide](https://redis.io/topics/quickstart)
2. In a separate terminal window run: `redis-server`. It should be running on port 6379. The app will not work if it is not running on port 6379
3. Make sure you have node and npm installed
4. Make sure you have a python 3 version installed
5. Clone the repository: `git clone https://github.com/mike2151/Online-OH-queue.git`
6. Go into the directory: `cd Online-OH-queue`
7. Optionally set up a [virtualenv](https://virtualenv.pypa.io/en/latest/) to develop this app
8. Run `pip install -r requirements.txt`
9. Run `npm install`
10. Navigate to `ohq/settings.py` and set the DEBUG variable at the top of the file to `True`
11. Run `npm run build`
12. Run `python manage.py makemigrations`
13. Run `python manage.py migrate`
14. Run `python manage.py runserver`
   
An instance of Online-OH-Queue should be running in port 8000

**Notes About Development:**
In development, emails are sent in the terminal so do not expect any emails to end up in your inbox.

If you make any changes to the UI, you must run `npm run build` in order for the changes to be visible. The app compiles react and then serves the compiled react.

When you push to github, make sure that the `.keep` files remain in `build/static/css` and `build/static/js`

## API
The following describes the endpoints for the API:

### Get Website Theme
Gets the theme for the website

<table>
    <tbody>
        <tr>
            <td>URL</td>
            <td><code>/api/v1/theme/</td>
        </tr>
        <tr>
            <td>HTTP Methods</td>
            <td>GET</td>
        </tr>
        <tr>
            <td>Permission</td>
            <td>Any</td>
        </tr>
        <tr>
            <td>Response Formats</td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>Parameters</td>
            <td>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Default</th>
                            <th>Description</th>
                            <th>Example Values</th>
                        </tr>
                    </thead>
                </table>
            </td>
        </tr>
    </tbody>
</table>

### Register User
Register a user for the site

<table>
    <tbody>
        <tr>
            <td>URL</td>
            <td><code>/api/v1/users/register/</td>
        </tr>
        <tr>
            <td>HTTP Methods</td>
            <td>POST</td>
        </tr>
        <tr>
            <td>Permission</td>
            <td>Any</td>
        </tr>
        <tr>
            <td>Response Formats</td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>Parameters</td>
            <td>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Default</th>
                            <th>Description</th>
                            <th>Example Values</th>
                        </tr>
                    </thead>
                    <tbody>
                      <tr>
                          <td><tt>email</tt></td>
                          <td><strong>Required</strong></td>
                          <td>School email of the user</td>
                          <td><tt>bob@seas.upenn.edu</tt></td>
                      </tr>
                      <tr>
                          <td><tt>first_name</tt></td>
                          <td><strong>Required</strong></td>
                          <td>First name of the user</td>
                          <td><tt>bob</tt></td>
                      </tr>
                      <tr>
                          <td><tt>last_name</tt></td>
                          <td><strong>Required</strong></td>
                          <td>Last name of the user</td>
                          <td><tt>smith</tt></td>
                      </tr>
                      <tr>
                          <td><tt>password</tt></td>
                          <td><strong>Required</strong></td>
                          <td>Password of the user</td>
                          <td><tt>password123</tt></td>
                      </tr>
                    </tbody>
                </table>
            </td>
        </tr>
    </tbody>
</table>

### Login User
Logs in a user to the site

<table>
    <tbody>
        <tr>
            <td>URL</td>
            <td><code>/api/v1/users/login/</td>
        </tr>
        <tr>
            <td>HTTP Methods</td>
            <td>POST</td>
        </tr>
        <tr>
            <td>Permission</td>
            <td>Any</td>
        </tr>
        <tr>
            <td>Response Formats</td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>Return</td>
            <td>Returns <code>token</code> , an authentication token for the user on success</td>
        </tr>
        <tr>
            <td>Parameters</td>
            <td>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Default</th>
                            <th>Description</th>
                            <th>Example Values</th>
                        </tr>
                    </thead>
                    <tbody>
                      <tr>
                          <td><tt>email</tt></td>
                          <td><strong>Required</strong></td>
                          <td>School email of the user</td>
                          <td><tt>bob@seas.upenn.edu</tt></td>
                      </tr>
                      <tr>
                          <td><tt>password</tt></td>
                          <td><strong>Required</strong></td>
                          <td>Password of the user</td>
                          <td><tt>password123</tt></td>
                      </tr>
                    </tbody>
                </table>
            </td>
        </tr>
    </tbody>
</table>

### Create Office Hours Queue
Creates an Office Hours Queue

<table>
    <tbody>
        <tr>
            <td>URL</td>
            <td><code>/api/v1/queue/create/</td>
        </tr>
        <tr>
            <td>HTTP Methods</td>
            <td>POST</td>
        </tr>
        <tr>
            <td>Response Formats</td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>Permission</td>
            <td>Admin</td>
        </tr>
        <tr>
            <td>Parameters</td>
            <td>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Default</th>
                            <th>Description</th>
                            <th>Example Values</th>
                        </tr>
                    </thead>
                    <tbody>
                      <tr>
                          <td><tt>name</tt></td>
                          <td><strong>Required</strong></td>
                          <td>Name of the office hours queue</td>
                          <td><tt>2 Minute Question Queue</tt></td>
                      </tr>
                      <tr>
                          <td><tt>times_open</tt></td>
                          <td><strong>Required</strong></td>
                          <td>Times that the queue is open</td>
                          <td>See section regarding hours</td>
                      </tr>
                    </tbody>
                </table>
            </td>
        </tr>
    </tbody>
</table>

### Keeps Office Hours Queue Open
Keeps Office Hours Queue Open

<table>
    <tbody>
        <tr>
            <td>URL</td>
            <td><code>/api/v1/queue/open/</td>
        </tr>
        <tr>
            <td>HTTP Methods</td>
            <td>POST</td>
        </tr>
        <tr>
            <td>Response Formats</td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>Permission</td>
            <td>TA</td>
        </tr>
        <tr>
            <td>Parameters</td>
            <td>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Default</th>
                            <th>Description</th>
                            <th>Example Values</th>
                        </tr>
                    </thead>
                    <tbody>
                      <tr>
                          <td><tt>queue</tt></td>
                          <td><strong>Required</strong></td>
                          <td>Name of the office hours queue</td>
                          <td><tt>2 Minute Question Queue</tt></td>
                      </tr>
                    </tbody>
                </table>
            </td>
        </tr>
    </tbody>
</table>

### Closes Office Hours Queue 
Closes Office Hours Queue 

<table>
    <tbody>
        <tr>
            <td>URL</td>
            <td><code>/api/v1/queue/close/</td>
        </tr>
        <tr>
            <td>HTTP Methods</td>
            <td>POST</td>
        </tr>
        <tr>
            <td>Response Formats</td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>Permission</td>
            <td>TA</td>
        </tr>
        <tr>
            <td>Parameters</td>
            <td>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Default</th>
                            <th>Description</th>
                            <th>Example Values</th>
                        </tr>
                    </thead>
                    <tbody>
                      <tr>
                          <td><tt>queue</tt></td>
                          <td><strong>Required</strong></td>
                          <td>Name of the office hours queue</td>
                          <td><tt>2 Minute Question Queue</tt></td>
                      </tr>
                    </tbody>
                </table>
            </td>
        </tr>
    </tbody>
</table>

### Ask A Question 
Creates a question for the office hours queue

<table>
    <tbody>
        <tr>
            <td>URL</td>
            <td><code>/api/v1/queue/&lt;name&gt;/ask</td>
        </tr>
        <tr>
            <td>HTTP Methods</td>
            <td>POST</td>
        </tr>
        <tr>
            <td>Response Formats</td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>Permission</td>
            <td>Authenticated</td>
        </tr>
        <tr>
            <td>Parameters</td>
            <td>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Default</th>
                            <th>Description</th>
                            <th>Example Values</th>
                        </tr>
                    </thead>
                    <tbody>
                      <tr>
                          <td><tt>name</tt></td>
                          <td><strong>Required - URL parameter</strong></td>
                          <td>Name of the office hours queue</td>
                          <td><tt>2-minute-office-hours-queue</tt></td>
                      </tr>
                      <tr>
                          <td><tt>description</tt></td>
                          <td><strong>Required</strong></td>
                          <td>The question itself (limited to 280 chars)</td>
                          <td>Question.</td>
                      </tr>
                    </tbody>
                </table>
            </td>
        </tr>
    </tbody>
</table>

### Get Current Office Hour Queues
Returns all of the active office hours queues along with their question

<table>
    <tbody>
        <tr>
            <td>URL</td>
            <td><code>/api/v1/queue/list/</td>
        </tr>
        <tr>
            <td>HTTP Methods</td>
            <td>GET</td>
        </tr>
        <tr>
            <td>Permission</td>
            <td>Authenticated</td>
        </tr>
        <tr>
            <td>Response Formats</td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>Return</td>
            <td>Returns list of office queue objects</td>
        </tr>
        <tr>
            <td>Parameters</td>
            <td>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Default</th>
                            <th>Description</th>
                            <th>Example Values</th>
                        </tr>
                    </thead>
                </table>
            </td>
        </tr>
    </tbody>
</table>

### Answer a question
Answers a question

<table>
    <tbody>
        <tr>
            <td>URL</td>
            <td><code>/api/v1/questions/answer</td>
        </tr>
        <tr>
            <td>HTTP Methods</td>
            <td>POST</td>
        </tr>
        <tr>
            <td>Permission</td>
            <td>TA</td>
        </tr>
        <tr>
            <td>Response Formats</td>
            <td>JSON</td>
        </tr>
       <tr>
            <td>Parameters</td>
            <td>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Default</th>
                            <th>Description</th>
                            <th>Example Values</th>
                        </tr>
                    </thead>
                    <tbody>
                      <tr>
                          <td><tt>queue</tt></td>
                          <td><strong>Required</strong></td>
                          <td>Name of the office hours queue that the question is in</td>
                          <td><tt>2-minute-office-hours-queue</tt></td>
                      </tr>
                      <tr>
                          <td><tt>question_id</tt></td>
                          <td><strong>Required</strong></td>
                          <td>Primary key of the question</td>
                          <td><tt>5</tt></td>
                      </tr>
                    </tbody>
                </table>
            </td>
        </tr>
    </tbody>
</table>

### Current Week's Questions
Gets the current week's questions at office hours to help TA's prepare for office hours

<table>
    <tbody>
        <tr>
            <td>URL</td>
            <td><code>/api/v1/summary/</td>
        </tr>
        <tr>
            <td>HTTP Methods</td>
            <td>GET</td>
        </tr>
        <tr>
            <td>Permission</td>
            <td>TA</td>
        </tr>
        <tr>
            <td>Response Formats</td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>Return</td>
            <td>Returns list of questions</td>
        </tr>
        <tr>
            <td>Parameters</td>
            <td>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Default</th>
                            <th>Description</th>
                            <th>Example Values</th>
                        </tr>
                    </thead>
                </table>
            </td>
        </tr>
    </tbody>
</table>