import json
import django.utils.timezone
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from authentication.models import User
from book_inventory_app.models import Author, Book,Stock
from book_inventory_app.apis.views import AuthorViewSet,BookViewSet,StockViewSet
from Utils import return_active_token
import datetime

class ApiAuthorViewTests(TestCase):

    def setUp(self):
        self.first_name = 'author'
        self.last_name = 'author'
        self.email = 'author@gmail.com'
        self.author = Author.objects.create(first_name=self.first_name,
                                          last_name=self.first_name,
                                          email=self.email
                                          )
        self.user_email = 'test@gmail.com'
        self.user_username = 'test'
        self.user_password = '123456'
        self.user = User.objects.create_user(email=self.user_email, password=self.user_password,
                                             username=self.user_username)

        self.login_data = {
            'email': self.user_email,
            'password': self.user_password
        }
        self.client = Client()
        self.token_url = reverse('authentication_apis:token_obtain_pair')
        self.auth =return_active_token(self.token_url,self.login_data,self.client)




    def test_user_view_set_unauthorized(self):
        """Test user view set that's not authorized"""
        api_request = APIRequestFactory().get("")
        detail_view = AuthorViewSet.as_view({'get': 'retrieve'})
        response = detail_view(api_request, pk=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_view_set_authorized(self):
        """Test user view set using force_authenticate"""
        factory = APIRequestFactory()
        user = User.objects.get(username=self.user_username)
        detail_view = AuthorViewSet.as_view({'get': 'retrieve'})

        # Make an authenticated request to the view...
        api_request = factory.get('')
        force_authenticate(api_request, user=user)
        response = detail_view(api_request, pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_author_info_api(self):
        """Test retrieving a user"""
        url = reverse('book_inv_apis:author-detail', kwargs={'pk':self.author.pk})

        self.client = Client(HTTP_AUTHORIZATION=self.auth,)
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_patch_author_info_api(self):
        """Test path a user"""
        data ={
            "first_name": "author-updated"
        }
        url = reverse('book_inv_apis:author-detail', kwargs={'pk': self.author.pk})
        self.client = Client(HTTP_AUTHORIZATION=self.auth,)
        resp = self.client.patch(url, data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_author_info_api(self):
        """Test update author"""
        data = {
                    "first_name": "author-updated",
                    "last_name": "author-updated",
                    "email": "author@gmail.com",
                    "date_of_birth":datetime.datetime.now()
                }

        url = reverse('book_inv_apis:author-detail', kwargs={'pk': self.author.pk})
        resp = self.client.put(url, data, HTTP_AUTHORIZATION=self.auth,content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


    def test_delete_author_info_api(self):
        """Test deleting author"""
        url = reverse('book_inv_apis:author-detail', kwargs={'pk': self.author.pk})
        self.client = Client(HTTP_AUTHORIZATION=self.auth,)
        resp = self.client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

class BookApiViewTests(TestCase):


    def setUp(self):
        self.first_name = 'author'
        self.last_name = 'author'
        self.email = 'author@gmail.com'
        self.author = Author.objects.create(first_name=self.first_name,
                                          last_name=self.first_name,
                                          email=self.email
                                          )
        self.book = Book.objects.create(title="Django for beginners",
                                            year_of_publication="2022",
                                            description="intro to django",
                                            author=self.author
                                            )

        self.user_email = 'test@gmail.com'
        self.user_username = 'test'
        self.user_password = '123456'
        self.user = User.objects.create_user(email=self.user_email, password=self.user_password,
                                             username=self.user_username)

        self.login_data = {
            'email': self.user_email,
            'password': self.user_password
        }
        self.client = Client()
        self.token_url = reverse('authentication_apis:token_obtain_pair')
        self.auth =return_active_token(self.token_url,self.login_data,self.client)




    def test_book_view_set_unauthorized(self):
        """Test book view set that's not authorized"""
        api_request = APIRequestFactory().get("")
        detail_view = BookViewSet.as_view({'get': 'retrieve'})
        response = detail_view(api_request, pk=self.book.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_view_set_authorized(self):
        """Test book view set using force_authenticate"""
        factory = APIRequestFactory()
        user = User.objects.get(username=self.user_username)
        detail_view = BookViewSet.as_view({'get': 'retrieve'})

        # Make an authenticated request to the view...
        api_request = factory.get('')
        force_authenticate(api_request, user=user)
        response = detail_view(api_request, pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_book_info_api(self):
        """Test retrieving a book"""
        url = reverse('book_inv_apis:book-detail', kwargs={'pk':self.book.pk})

        self.client = Client(HTTP_AUTHORIZATION=self.auth,)
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_patch_book_info_api(self):
        """Test patch a book"""
        data ={
            "title": "book-updated"
        }
        url = reverse('book_inv_apis:book-detail', kwargs={'pk': self.book.pk})
        self.client = Client(HTTP_AUTHORIZATION=self.auth,)
        resp = self.client.patch(url, data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_book_info_api(self):
        """Test update a book"""
        data = json.dumps({
                    "title": "title-updated",
                    "year_of_publication": "2023",
                    "description": "description-updated",
                    "author":self.author.id
                })
        url = reverse('book_inv_apis:book-detail', kwargs={'pk': self.book.pk})
        resp = self.client.put(url, data, HTTP_AUTHORIZATION=self.auth,content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


    def test_delete_book_info_api(self):
        """Test deleting book"""
        url = reverse('book_inv_apis:book-detail', kwargs={'pk': self.book.pk})
        self.client = Client(HTTP_AUTHORIZATION=self.auth,)
        resp = self.client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)


class StockApiViewTests(TestCase):


    def setUp(self):
        self.first_name = 'author'
        self.last_name = 'author'
        self.email = 'author@gmail.com'
        self.author = Author.objects.create(first_name=self.first_name,
                                          last_name=self.first_name,
                                          email=self.email
                                          )
        self.book = Book.objects.create(title="Django for beginners",
                                            year_of_publication="2022",
                                            description="intro to django",
                                            author=self.author
                                            )

        self.stock = Stock.objects.create(book=self.book,
                                        quantity=10,
                                        description="intro to Django",
                                        status='Good'
                                        )

        self.user_email = 'test@gmail.com'
        self.user_username = 'test'
        self.user_password = '123456'
        self.user = User.objects.create_user(email=self.user_email, password=self.user_password,
                                             username=self.user_username)

        self.login_data = {
            'email': self.user_email,
            'password': self.user_password
        }
        self.client = Client()
        self.token_url = reverse('authentication_apis:token_obtain_pair')
        self.auth =return_active_token(self.token_url,self.login_data,self.client)

    def test_stock_view_set_unauthorized(self):
        """Test stock view set that's not authorized"""
        api_request = APIRequestFactory().get("")
        detail_view = StockViewSet.as_view({'get': 'retrieve'})
        response = detail_view(api_request, pk=self.stock.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_stock_view_set_authorized(self):
        """Test stock view set using force_authenticate"""
        factory = APIRequestFactory()
        user = User.objects.get(username=self.user_username)
        detail_view = StockViewSet.as_view({'get': 'retrieve'})

        # Make an authenticated request to the view...
        api_request = factory.get('')
        force_authenticate(api_request, user=user)
        response = detail_view(api_request, pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_stock_info_api(self):
        """Test retrieving a stock"""
        url = reverse('book_inv_apis:stock-detail', kwargs={'pk':self.stock.pk})

        self.client = Client(HTTP_AUTHORIZATION=self.auth,)
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_patch_stock_info_api(self):
        """Test patch a stock"""
        data ={
            "description": "Django intro -updated"
        }
        url = reverse('book_inv_apis:stock-detail', kwargs={'pk': self.stock.pk})
        self.client = Client(HTTP_AUTHORIZATION=self.auth,)
        resp = self.client.patch(url, data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_stock_info_api(self):
        """Test update stock"""
        data = json.dumps({
                    "book": self.book.id,
                    "quantity": 18,
                    "description": "description-updated-twice",
                    "status":'Bad'
                })
        url = reverse('book_inv_apis:stock-detail', kwargs={'pk': self.stock.pk})
        resp = self.client.put(url, data, HTTP_AUTHORIZATION=self.auth,content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


    def test_delete_stock_info_api(self):
        """Test deleting stock: should not accept deletion of stock"""
        url = reverse('book_inv_apis:stock-detail', kwargs={'pk': self.stock.pk})
        self.client = Client(HTTP_AUTHORIZATION=self.auth,)
        resp = self.client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)