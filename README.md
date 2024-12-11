# WS2024 - Principles of AI Engineering

## Run app with Development Database  
- [ ] Install conda and create a virtual enviroment
- [ ] Install all depedences using requirements.txt file
- [ ] Create a development database from the sql script at the root of this project directory 
- [ ] Run the flask development server using these command line inputs below 

```
TICKET_ENV=dev TICKET_MYSQL_USER=ticket_dev TICKET_MYSQL_PWD=ticket_dev_pwd TICKET_MYSQL_HOST=localhost TICKET_MYSQL_DB=ticket_dev_db python3 -m api.app
```
## Running tests on the app
```
TICKET_ENV=test TICKET_MYSQL_USER=ticket_test TICKET_MYSQL_PWD=ticket_test_pwd TICKET_MYSQL_HOST=localhost TICKET_MYSQL_DB=ticket_test_db python3 -m unittest
```

## Usage  
Here we demonstrate how to send requests to the api and receive responses
```

```
