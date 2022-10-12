from django.test import SimpleTestCase
from django.urls import reverse, resolve

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from authentication.apis.views import RegisterUserAPIView,UserViewSet


class ViewUrlTests(SimpleTestCase):
    """Authentication Urls Test Cases."""

    def test_token_url_is_resolved(self):
        """Test resolving token url."""
        url = reverse('authentication_apis:token_obtain_pair')
        self.assertEquals(resolve(url).func.view_class, TokenObtainPairView)

    def test_token_refresh_url_is_resolved(self):
        """Test resolving token_refresh url."""
        url = reverse('authentication_apis:token_refresh')
        self.assertEquals(resolve(url).func.view_class, TokenRefreshView)

    def test_user_registration_url_is_resolved(self):
        """Test resolving user registration."""
        url = reverse('authentication_apis:user-registration')
        self.assertEquals(resolve(url).func.view_class, RegisterUserAPIView)
