## OBA-API (Offline Business Analyzer)

OBA RestFul APIs built with Flask and Python.
-   Live API can be found here https://bit.ly/32sEFr2
-   Documentation can be found here  https://bit.ly/32oZGTm

## Overview
This is a RestApi for performing basic business transactions and computations such as:

-   Register a business.
-   Upload a file. (csv)
-   Get Top-performing items by value and quantity   

HTTP |End Point  | Result
--- | --- | ----------
GET | `/v1/` | Index route returns welcome message.
POST | `/v1/register` | Registers a new user and assigns them an account.
GET | `/v1/users` | Returns all users.
GET | `/v1/users/<user_id>` | Returns a particular user matching the given User ID.
GET | `/v1/businesses/all` | Returns all registered businesses.
POST | `/v1/business/<int:id>/upload` | Upload a .csv file and store data.
GET | `/v1//business/<int:id>/uploads` | Returns a list of all uploaded files.
GET | `/v1/business/register` | Registers a new user and assigns them an account.
PUT | `/v1/business/amount/incoming/<int:days>` | Returns the amount incoming over a specific number of days.
PUT | `/v1/business/amount/outgoing/<int:days>` | Returns the amount outgoing(expenditure) over a specific number of days.
PUT | `/v1/business/<int:id>` | Update business data.
POST | `/v1/login` | Logs in registered user and returns a token.
GET | `/v1/business/<int:id>/value` | Returns top 5 items from transactions by value
GET | `/v1/business/<int:id>/quantity` | Returns top 5 items from transactions by quantity.
POST | `/v1/logout` | Logs out current user and deletes user session.
DELETE | `/v1/business/<int:id>` | Deletes business that matches the provided ID.
DELETE | `/v1/business/<int:id>/<filename>` | Deletes Uploaded file data specified by name.

## Installation

 ## Requirements:

* Python 3.7
* pip
* virtualenv
* postgresql

## Run application on Local
1. clone repo. `$ git clone https://github.com/Awesome94/bank-API.git`

    `cd oba-python-api/`

2. Create and activate a virtual environment and install requirements:

    - `$ mkvirtualenv <name_of_your_choice>`

    - `$ pip install -r requirements.txt.`

3. create a local database and run migrations:
    - `$ createdb bankapi`
        - `flask db init`
        - `flask db migrate`
        - `flask db upgrade`


    NB: Make sure you have FLASK_APP set as `app/__init__.py`.


4. Start your application



    $ flask run
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader

You can now open the API with Curl from the command line:
or Postman.

    $ using Curl

    $ curl -X GET http://127.0.0.1:5000/v1/
    [{"url": "http://127.0.0.1:5000/v1/", "text": "Welcome"}

