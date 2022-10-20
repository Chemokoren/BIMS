from django.test import TestCase, Client
from rest_framework.response import Response
from rest_framework.reverse import reverse

from authentication.models import User
from enum import Enum

def return_active_token(token_url, data, client):
    """Method returns an active access token after a successful login."""
    response = client.post(token_url, data, format='json')
    auth = 'Bearer {0}'.format(response.data['access'])
    return auth


class Status(Enum):
    GOOD          = 'Good'
    BAD           = 'Bad'
    CRITICAL      = 'Critical'
    OUT_OF_STOCK  = 'out of stock'

def evaluate_stock_status(quantity):
    """Takes in the stock quantity and returns the corresponding status."""
    quantity =validate_number(quantity)
    status=None
    if quantity >=10:
        status =Status.GOOD
    elif quantity >=5 and quantity < 10:
        status =Status.BAD
    elif quantity >= 1 and quantity < 5:
        status =Status.CRITICAL
    elif quantity <= 0:
        status =Status.OUT_OF_STOCK
    return status

def validate_number(val):
    """validate if val is a number"""
    try:
        num = float(val)

        return num
    except ValueError:
        return Response({'message':'value provided is not a number'})