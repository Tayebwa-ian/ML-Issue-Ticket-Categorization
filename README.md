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
 curl -s -H "Content-Type: application/json" -X POST -d '{"title":"Contrast for Select files to upload button is too low", "author":"MEMBER", "body":"The contrast ratio for the Select files to upload is on 2.69 and does not meet the minimum for WCAG AA."}' http://127.0.0.1:5000/api/core/predict  
{
    "url": null,
    "created_at": "2024-12-29 21:24:57",
    "title": "Contrast for Select files to upload button is too low",
    "author": "MEMBER",
    "actual_label": null,
    "prediction": "Bug",
    "body": "The contrast ratio for the Select files to upload is on 2.69 and does not meet the minimum for WCAG AA.",
    "id": "1",
    "updated_at": "2024-12-29 21:24:57"
}  
  
curl -s http://127.0.0.1:5000/api/core/predict  
[
    {
        "title": "Contrast for Select files to upload button is too low",
        "updated_at": "2024-12-29 21:24:57",
        "body": "The contrast ratio for the Select files to upload is on 2.69 and does not meet the minimum for WCAG AA.",
        "prediction": "Bug",
        "id": "1",
        "created_at": "2024-12-29 21:24:57",
        "actual_label": null,
        "url": null,
        "author": "MEMBER"
    }
]  
  
curl -s http://127.0.0.1:5000/api/core/issues/1  
{
    "url": null,
    "created_at": "2024-12-29 21:24:57",
    "title": "Contrast for Select files to upload button is too low",
    "author": "MEMBER",
    "actual_label": null,
    "prediction": "Bug",
    "body": "The contrast ratio for the Select files to upload is on 2.69 and does not meet the minimum for WCAG AA.",
    "id": "1",
    "updated_at": "2024-12-29 21:24:57"
}  


```
