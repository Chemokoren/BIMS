from django.db import models

from django.db import models
from django.utils.timezone import datetime, timedelta
from django.utils.text import slugify
import django.utils.timezone
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Override the `create_user` function for creating `User` objects."""

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User Model"""
    first_name          = models.CharField(db_index=True, max_length=255, unique=False)
    last_name           = models.CharField(db_index=True, max_length=255, unique=False)
    username            = models.CharField(db_index=True, max_length=255, unique=True)
    slug                = models.SlugField(max_length=100, unique=True, blank=True)
    email               = models.EmailField(db_index=True, unique=True)
    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField('staff status', default=False)
    date_of_birth       = models.DateTimeField(null=True, blank=True, default=django.utils.timezone.now)
    phone               = models.CharField(max_length=200, null=True, blank=True)
    additional_phone    = models.CharField(max_length=200, null=True, blank=True)
    country             = models.CharField(db_index=True, max_length=255, unique=False)
    time_zone           = models.CharField(max_length=200, null=True, blank=True)
    city                = models.CharField(max_length=200, null=True, blank=True)
    address             = models.CharField(max_length=200, null=True, blank=True)
    zip_code            = models.CharField(max_length=200, null=True, blank=True)
    date_joined         = models.DateTimeField(default=timezone.now)
    created_on          = models.DateTimeField(auto_now_add=True)
    updated_on          = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','username']

    def save(self, *args, **kwargs):
        """Overriding the save method to update slug field"""
        self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)

    # informs the UserManager class defined above should manage objects of this type.
    objects = UserManager()

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        """user absolute url"""
        return reverse("authentication_apis:user-detail", args=[str(self.id)])

    def __str__(self):
        """returns a string representation of the `User`."""
        return str(self.username)

    @property
    def get_full_name(self):
        """this is the user's first and last name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_user_short_name(self):
        """this is the first name"""
        return f"{self.first_name}"
