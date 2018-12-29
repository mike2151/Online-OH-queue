[![Build Status](https://travis-ci.org/mike2151/Online-OH-queue.svg?branch=master)](https://travis-ci.org/mike2151/Online-OH-queue)

# Online Office Hours Queue
##### Table of Contents 
[Setup](#Setup) 
<a name="Setup"/> <br/>
[Office Hours Queue Setup](#OHQueueSetUp) 
<a name="OHQueueSetUp"/> <br/>
[Theme Configuration](#Theme) 
<a name="Theme"/> <br/>
[Development](#Development) 
<a name="Development"/><br/>
[API](#API) 
<a name="API"/>

## Setup

domain in admin site

## OHQueueSetUp
Online-OH-Queue supports the creation of multiple queues. To create a queue, navigate to `/admin`, log in with the superuser credentials you created earlier or with another admin account.

Then, click on `+ Add` in the `OHQUEUE` section. <br />
Enter a name for the queue. This name will be visibile to all students. <br />
Do not enter any questions. Ignore this field <br />
Do not enter the average wait time. Ignore this field. This will be automatically done by the server <br /><br />
Times Open Section: <br />
This field is used to specify when the queue is open for students to ask questions. You must enter a string in the following format: <br />
Example: `Monday:2:00pm-4:00pm;5:00pm-7:00pm Tuesday:11:30am-5:00pm Wednesday:11:30am-5:00pm Thursday:11:30am-5:00pm Friday:11:30am-5:00pm Saturday: Sunday: ` <br />
In the queue above, office hours are held 2pm to 4pm and 5pm to 7pm on Monday. On Tuesday to Friday, office hours are held  11:30 am to 5pm. There are no office hours held on Saturday or Sunday. <br />
Notes on the format: <br />
You must include **ALL** days of the week in the times open field. If there no office hours being held on that day, then leave a space after the colon. <br />
When specifing times, use the format above: hour:minuteam/pm. First indicate the hour. Next, a colon followed by the minutes. Next, either am or pm. The dash indicates a time range. So in the case of `2:00pm-4:00pm` the queue remains open from 2pm to 4pm. <br />
A semicolon followed by another time range is used if the queue is not open during a continuous time interval. See Monday for an example <br />
A space is followed after specifing a day of open times. <br />
**Failure to adhere to the time convention will make the Office Hours Queue not appear or may even bring up a failure error on the office hours page!**



## Theme
By default, the Online-OH-Queue comes with a green color theme. This can be changed. Navigate to the `style.css` file located in `src/static/css/style.css` and in `frontend/static/style.css`. You must make changes to both files!

At the top of the file are theme variables which you can edit to change the theme of the website. 
Theme variables: <br />
`primary-color`: This is the main color of the website. By default it is the green color.

## Development
To develop for Online-OH-Queue, do the following steps:
1. Clone the repository
2. Run `pip install -r requirements.txt`
3. Run `npm install`
4. Run `npm run build`
5. Run `python manage.py runserver`
   
An instance of Online-OH-Queue should be running in port 8000

## API
The following describes the endpoints for the API:

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

### Closes Office Hours Queue Early
Closes Office Hours Queue Early

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