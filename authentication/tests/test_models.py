from django.test import TestCase

from authentication.models import User
from django.contrib.auth.hashers import make_password
from django.urls import reverse, resolve

class TestModel(TestCase):

    def setUp(self):
        user_password = make_password('123456')
        self.user = User.objects.create(
                    first_name ='test',
                    last_name='test',
                    username='test slug 1',
                    password =user_password,
                    email ='slugtest@gmail.com'
        )


    def test_should_create_user(self):
        """Test if user is created successfully"""
        self.assertEqual(str(self.user), self.user.username)
#
    def test_user_is_assigned_slug_on_creation(self):
        """Test if user is assigned slug on creation"""
        self.assertEquals(self.user.slug, 'test-slug-1')

    def test_get_full_name(self):
        """Test user's full name"""
        self.assertEquals(self.user.get_full_name, '{0} {1}'.format("test", "test"))

    def test_get_short_name(self):
        """Test user's short name"""
        self.assertEquals(self.user.get_user_short_name(), self.user.first_name)

    def test__str__(self):
        """Test user's __str__ method"""
        self.assertEquals(self.user.__str__(), self.user.username)

    def test_get_absolute_url(self):
        """Test user's absolute url"""
        user = User.objects.get(id=self.user.id)
        url = reverse('authentication_apis:user-detail', args=[self.user.id])
        self.assertEqual(user.get_absolute_url(), url)
