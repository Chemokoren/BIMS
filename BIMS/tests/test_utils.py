from django.test import TestCase
from Utils import evaluate_stock_status, Status
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
