
# Restful API for Bookstore Inventory Management System

This is the design & implementation of a bookstore inventory management system.

# Setup
1. Clone the project using the approach most flexible to you or simply downlod
2. Setup your virtual environment
3. cd to the project's root directory
4. Add DEBUG, SECRET_KEY to .env file
5. Add ALLOWED_HOSTS e.g. '127.0.0.1' when testing in your localhost 
6. Run the requirements.txt file using the following command

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

## Testing on Postman

On the project's root you will find the collection file named as follows:

```
JamboPay.postman_collection.json
```

Import it to your Postman App and test any of the endpoints.


## Running Automated Tests

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
/api/v1/docs/

