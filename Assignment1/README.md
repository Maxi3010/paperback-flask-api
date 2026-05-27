# Paperback Flask API

Newspaper issue and subscription management API built with Flask and Flask-RESTX.

## Assignment 1
## Deadline: <span style="color:red;">14.04.2024, 23:00</span>

--- 

# PaperBack: A Newspaper Subscription Management Software

Let us imagine, that we are building up an application to manage newspaper subscriptions.
The software shall be used by employees of the newspaper agency to manage the newspaper 
issues and monitor their client subscriptions.
This programming task is about implementing a web API, so that the same software can be
customized by different newspaper agencies to build their own applications based on the provided API. 
At the moment, we do not care about the front-end of the application, which could be 
any browser or a mobile app. And we also don’t care about a database that stores the data 
persistently. In this exercise, we deal with the API implementation only. 
You may use a REST client like Postman to quickly see the results of the API call. 
It is recommended to use Python requests library and Pytest to thoroughly test the API. 
A Swagger based UI is provided, so that you can also test the application based on a 
browser front-end. Design your objects and classes allowing for easy future extensions.

## Functionality

The API consists of the following main functionality

**Management of newspapers and issues**
- Add/remove/update a new newspaper. Each paper has a (unique) paper ID, name, issue frequency (in days), and monthly price
- Add/remove/update an issue of a newspaper. Each issue has a publication date, number of pages, etc
- Each issue has an editor (i.e. the responsible person; see below)
- Initially, paper issues are not published, but once updated, they can be delivered to subscribers

**Management of editors**
- Add/remove/update editors to/from the system. Each editor has a (unique) editor-id, name, address and a list of newspapers, s/he can work for care of.
- When an editor is removed (e.g., quits the job), transfer all issues in his/her supervision to another editor of the same newspaper.

**Management of subscribers**
- Add/remove subscribers to/from the system. Each subscriber has a (unique) subscriber ID, name, address and a list of newspapers that they are subscribed to.
- Each client can choose to subscribe to special issues
- When a client is removed (e.g., cancels a subscription), all subscriptions are stopped


## Your Task

The API should be implemented in Python using a package called Flask, which allows you to define 
HTML methods GET, POST, PUT etc. Each method returns a JSON object, which can be used by 
the front-end application in adequate ways. The summary of HTML methods to be implemented 
as part of the homework is listed in the following table. 

The first few methods have already been implemented as examples.
Write Test cases to thoroughly test your API – 
manual testing with Postman is good, but not enough.
Come up with an automated testing script, which simulates the daily operations 
of the paper agency. For example, add newspapers, employees and clients, 
create issues and subscriptions.

> [!NOTE]
> In this exercise, we focus on the API implementation only. 
Feel free to create your own client application based on the API as your side project. 
The side project is not graded but a lot of fun!

## Your Task
Your task is to assert that the following HTTP methods are implemented and functioning.
Ensure the correct functionality through appropriate test cases!

A few examples are provided in the [`src`](./src) and [`test`](./test) folders to get you started.

| Endpoint                                         | HTTP Method | Description                                                                                                                                             |
|--------------------------------------------------|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/newspaper`                                     | `GET`       | List all newspapers in the agency.                                                                                                                      |
| `/newspaper`                                     | `POST`      | Create a new newspaper.                                                                                                                                 |
| `/newspaper/<paper_id>`                          | `GET`       | Get a newspaper's information.                                                                                                                          |
| `/newspaper/<paper_id>`                          | `POST`      | Update a new newspaper.                                                                                                                                 |
| `/newspaper/<paper_id>`                          | `DELETE`    | Delete a newspaper, and all its issues.                                                                                                                 |
| `/newspaper/<paper_id>/issue`                    | `GET`       | List all issues of a specific newspaper.                                                                                                                |
| `/newspaper/<paper_id>/issue`                    | `POST`      | Create a new issue.                                                                                                                                     |
| `/newspaper/<paper_id>/issue/<issue_id>`         | `GET`       | Get information of a newspaper issue                                                                                                                    |
| `/newspaper/<paper_id>/issue/<issue_id>/release` | `POST`      | Release an issue                                                                                                                                        |
| `/newspaper/<paper_id>/issue/<issue_id>/editor`  | `POST`      | Specify an editor for an issue. (Transmit the editor ID as parameter)                                                                                   |
| `/newspaper/<paper_id>/issue/<issue_id>/deliver` | `POST`      | "Send" an issue to a subscriber. This means there should be a record of the subscriber receiving                                                        |
| `/newspaper/<paper_id>/stats`                    | `GET`       | Return information about the specific newspaper (number of subscribers, monthly and annual revenue)                                                     |
| `/editor`                                        | `GET`       | List all editors of the agency.                                                                                                                         |
| `/editor`                                        | `POST`      | Create a new editor.                                                                                                                                    |
| `/editor/<editor_id>`                            | `GET`       | Get an editor's information.                                                                                                                            |
| `/editor/<editor_id>`                            | `POST`      | Update an editor's information.                                                                                                                         |
| `/editor/<editor_id>`                            | `DELETE`    | Delete an editor.                                                                                                                                       |
| `/editor/<editor_id>/issues`                     | `GET`       | Return a list of newspaper issues that the editor was responsible for.                                                                                  |
| `/subscriber`                                    | `GET`       | List all subscribers in the agency.                                                                                                                     |
| `/subscriber`                                    | `POST`      | Create a new subscriber.                                                                                                                                |
| `/subscriber/<subscriber_id>`                    | `GET`       | Get a subscriber's information.                                                                                                                         |
| `/subscriber/<subscriber_id>`                    | `POST`      | Update a subscriber's information.                                                                                                                      |
| `/subscriber/<subscriber_id>`                    | `DELETE`    | Delete a subscriber.                                                                                                                                    |
| `/subscriber/<subscriber_id>/subscribe`          | `POST`      | Subscribe a subscriber to a newspaper. (Transmit the newspaper ID as parameter.)                                                                        |
| `/subscriber/<subscriber_id>/stats`              | `GET`       | Get the number of newspaper subscriptions and the monthly and annual cost, as well as the number of issues that the subscriber received for each paper. |
| `/subscriber/<subscriber_id>/missingissues`      | `GET`       | Check if there are any undelivered issues of the subscribed newspapers.                                                                                 |


### Submission
Submission of the project must be done through a Github Repository.
Create your own repository and upload your code to your private repository before the deadline. 
Add [@deepak-dhungana](https://github.com/deepak-dhungana) and [@stklik](https://github.com/stklik) as collaborators to your repository. 

**Submit the URL of your repository via MS Teams.**

In order to create a new Github account, visit https://github.fhkre.ms and login with your IMC FH Krems account.


---
## Technical Hints

We developed our application using [flask-restx](https://flask-restx.readthedocs.io/en/latest).

#### Python Version
You will (probably) not need any special features related to specific Python versions to complete this exercise.
The sample code provided by us was developed in Python v3.8 for general compatibility.
Feel free, however, to use a newer version (e.g. 3.9, 3.10, 3.11) to benefit from new functionality.


### Singletons
The app uses a programming pattern called "Singleton" (see [Wikipedia](https://en.wikipedia.org/wiki/Singleton_pattern)) 
to assert that all information is stored in the same `Agency` object.
To access the (globally unique) agency, use the `Agency.get_instance()` *static* method.


### Installation

You should not need any packages beyond those in [requirements.txt](./requirements.txt) 
to get started.

### Run the webserver

You can start the app by executing
```bash
python start.py
```

Then, you can navigate to http://127.0.0.1:7890/ and try the endpoints using the Swagger interface.


### Testing with [pytest](https://docs.pytest.org/)

To trigger the automated tests, execute
```bash
pytest
```

Note, that your `print` statements will not be visible, 
unless you add the `-s` argument to the call, i.e. `pytest -s`.


## Contribute

Should you discover any problems in the code or have suggestions, 
please leave a Github issue and document your findings.

If you have a fix for a problem, feel free to leave a Pull Request. 
([Helpful Docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request))
