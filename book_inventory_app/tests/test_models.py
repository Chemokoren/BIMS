from django.test import TestCase

from book_inventory_app.models import Author,Book,Stock
from django.contrib.auth.hashers import make_password
from django.urls import reverse, resolve

class AuthorModelTestcase(TestCase):
    """Test the Author Model"""
    @classmethod
    def setUpTestData(cls):
        """Create Author's test data"""
        Author.objects.create(first_name="ann", last_name="brown", email="annbrown@gmail.com")

    def test_string_method(self):
        """Test Author's __str__ method"""
        author = Author.objects.get(id=1)
        expected_string = f"Author: {author.first_name} {author.last_name}"
        self.assertEqual(str(author), expected_string)

    def test_get_absolute_url(self):
        """Test Author's absolute url"""
        author = Author.objects.get(id=1)
        url = reverse('book_inv_apis:author-detail', kwargs={'pk': 1})
        self.assertEqual(author.get_absolute_url(), url)

class BookModelTestcase(TestCase):
    """Tests for the Book Model"""
    @classmethod
    def setUpTestData(cls):
        """Create Book's test data"""
        author= Author.objects.create(first_name="ann", last_name="brown", email="annbrown@gmail.com")
        Book.objects.create(title="python -intro", year_of_publication="2022", description="python basis", author=author)


    def test_string_method(self):
        """Test Book's __str__ method"""
        book = Book.objects.get(id=1)
        expected_string = f"Book: {book.title}"
        self.assertEqual(str(book), expected_string)

    def test_get_absolute_url(self):
        """Test Book's absolute url"""
        book = Book.objects.get(id=1)
        url = reverse('book_inv_apis:book-detail', kwargs={'pk': 1})
        self.assertEqual(book.get_absolute_url(), url)

class StockModelTestcase(TestCase):
    """Tests for the Stock Model"""
    @classmethod
    def setUpTestData(cls):
        """Create Stock's test data"""
        author= Author.objects.create(first_name="ann", last_name="brown", email="annbrown@gmail.com")
        book=Book.objects.create(title="python -intro", year_of_publication="2022", description="python basis", author=author)
        Stock.objects.create(book=book, quantity="20", description="python basis", status='Good')

    def test_string_method(self):
        """Test Stock's __str__ method"""
        stock = Stock.objects.get(id=1)
        expected_string = f"Stock: {stock.description}"
        self.assertEqual(str(stock), expected_string)

    def test_get_absolute_url(self):
        """Test Stock's absolute url"""
        stock = Stock.objects.get(id=1)
        url = reverse('book_inv_apis:stock-detail', kwargs={'pk': 1})
        self.assertEqual(stock.get_absolute_url(), url)
