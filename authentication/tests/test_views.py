from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from authentication.models import User
from authentication.apis.views import UserViewSet
import json

class BaseTestCase(TestCase):

    def setUp(self):
        self.email = 'test@gmail.com'
        self.username = 'test'
        self.password = '123456'
        self.user = User.objects.create_user(email=self.email, password=self.password, username=self.username)

        self.data = {
            'email': self.email,
            'password': self.password
        }
        self.client = Client()
        self.token_url = reverse('authentication_apis:token_obtain_pair')
        self.logout_url = reverse('authentication_apis:logout')


class ApiViewTests(BaseTestCase):
    """Authentication API Views Test Cases"""

    def return_active_token(self):
        """Method returns an active access token after a successful login."""
        response = self.client.post(self.token_url, self.data, format='json')
        auth = 'Bearer {0}'.format(response.data['access'])
        return auth

    def test_login(self):
        """Test user login"""
        response = self.client.post(self.token_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        """Test user logout:blacklist refresh token"""
        token_info = self.client.post(self.token_url, self.data, format='json')
        auth = 'Bearer {0}'.format(token_info.data['access'])
        response = self.client.post(self.logout_url,token_info.data, HTTP_AUTHORIZATION=auth,
                                   format='json')
        self.assertEquals(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_jwt_login_custom_response_json(self):
        """Test & ascertain that JWT login using JSON POST works."""
        response = self.client.post(self.token_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_view_set_unauthorized(self):
        """Test user view set that's not authorized"""
        api_request = APIRequestFactory().get("")
        detail_view = UserViewSet.as_view({'get': 'retrieve'})
        response = detail_view(api_request, pk=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_view_set_authorized(self):
        """Test user view set using force_authenticate"""
        factory = APIRequestFactory()
        user = User.objects.get(username=self.username)
        detail_view = UserViewSet.as_view({'get': 'retrieve'})

        # Make an authenticated request to the view...
        api_request = factory.get('')
        force_authenticate(api_request, user=user)
        response = detail_view(api_request, pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_info_api(self):
        """Test retrieving a user"""
        url = reverse('authentication_apis:user-detail', kwargs={'pk':self.user.pk})
        auth =self.return_active_token()
        self.client = Client(HTTP_AUTHORIZATION=auth,)
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_patch_user_info_api(self):
        """Test path a user"""
        data ={
            "username": "test-updated",
            "email": "test@gmail.com",
            'password': "masai123",
            'password2': "masai123"
        }
        url = reverse('authentication_apis:user-detail', kwargs={'pk': self.user.pk})
        auth =self.return_active_token()
        self.client = Client(HTTP_AUTHORIZATION=auth,)
        resp = self.client.patch(url, data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_user_info_api(self):
        """Test path a user"""
        data = json.dumps({
                    "username": "test-updated-3",
                    "email": "test@gmail.com",
                    "first_name": "test",
                    "last_name": "test",
                    'password': "12345678$$",
                    'password2': "12345678$$"
                })
        url = reverse('authentication_apis:user-detail', kwargs={'pk': self.user.pk})
        auth =self.return_active_token()
        resp = self.client.put(url, data, HTTP_AUTHORIZATION=auth,content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


    def test_delete_user_info_api(self):
        """Test deleting a user"""
        url = reverse('authentication_apis:user-detail', kwargs={'pk': self.user.pk})
        auth =self.return_active_token()
        self.client = Client(HTTP_AUTHORIZATION=auth,)
        resp = self.client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)