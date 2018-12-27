# Online Office Hours Queue
##### Table of Contents 
[Setup](#Setup) 
<a name="Setup"/> <br/>
[Theme Configuration](#Theme) 
<a name="Theme"/> <br/>
[Development](#Development) 
<a name="Development"/><br/>
[API](#API) 
<a name="API"/>

## Setup

## Theme
By default, the Online-OH-Queue comes with a green color theme. This can be changed. Navigate to the `style.css` file located in `src/style/style.css`. 

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