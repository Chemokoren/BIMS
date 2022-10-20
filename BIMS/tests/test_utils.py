from django.test import TestCase
from Utils import evaluate_stock_status, Status,validate_number
class UtilsTestcase(TestCase):
    """Testing the Utils"""

    def test_good_status(self):
        """Test if status is Good"""
        quantity =20
        res_status= evaluate_stock_status(quantity)
        self.assertEqual(res_status.value,Status.GOOD.value)

    def test_bad_status(self):
        """Test if status is BAD"""
        quantity =7
        res_status= evaluate_stock_status(quantity)
        self.assertEqual(res_status.value,Status.BAD.value)

    def test_criticial_status(self):
        """Test if status is Critical"""
        quantity =3
        res_status= evaluate_stock_status(quantity)
        self.assertEqual(res_status.value,Status.CRITICAL.value)

    def test_out_of_stock_status(self):
        """Test if status is Out of Stock"""
        quantity =-9
        res_status= evaluate_stock_status(quantity)
        self.assertEqual(res_status.value,Status.OUT_OF_STOCK.value)

    def test_is_invalid_number(self):
        """Test if the provided input is an invalid number"""
        input_val ="mine"
        res =validate_number(input_val).data['message']
        self.assertEqual(res,"value provided is not a number")

    def test_is_valid_number(self):
        """Test if the provided input is a valid number"""
        input_val ="25"
        res =validate_number(input_val)
        self.assertEqual(res,25)

