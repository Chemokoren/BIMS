
# Restful API for Bookstore Inventory Management System

This is the design & implementation of a bookstore inventory management system.

# Setup
1. Clone the project using the approach most flexible to you or simply downlod

2. Setup your virtual environment

3. cd to the project's root directory

4. Run the requirements.txt file using the following command

```
pip install -r requirements.txt
```
5. Run migrations



## Deployment

To deploy this project run

```bash
  python manage.py runserver
```


## Demo

1. Register a test user using the following url
/api/v1/register/

2. Generate access token using the link
/api/v1/token/

3. Use the access token to query the rest of the api's on authors,books and stock.


## Running Tests

To run tests, run any of the following commands
based on your needs

```bash
  python manage.py test

  coverage run manage.py test

  coverage run manage.py test -v 2

  coverage run manage.py test -v 2 && coverage report

  coverage run --source "RESTAPI" manage.py test -v 2 && coverage report

  coverage run --source "RESTAPI" manage.py test -v 2 && coverage report && coverage html

```


## API Reference

#### You can access the API reference using the following link:~
/api/v1/swagger/schema/

