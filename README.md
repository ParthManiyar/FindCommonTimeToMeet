# FindCommonTimeToMeet
To run the web application follow below steps:
* git clone https://github.com/ParthManiyar/findCommonTimeToMeet.git
* docker-compose up --build
* Now we can play with API with postman collection [here](https://www.getpostman.com/collections/27bf85ab792836876e44 "Title").

To Install all the dependecies(optional):
> pip install -r requirements.txt

To run the API server externally:
> python manager.py runserver

To clear the database:
> python manage.py flush

To cerate the db tables again:
> python manage.py makemigrations

> python manage.py migrate

To run the unit test
> python manage.py test

# Assumptions:
For suggested-time API
* Assumed that body request and response will be in IST format as example given in the problem statement.
* Calendar Information provided post request will always be valid. 
* Calendar Information of the same day only .
* day_start_time will be less than day_end_time.
* slots provided will be of the same day

  
