from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils.translation import gettext_lazy as _
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models


# setup a custom User Model to house what we want
class UserManager(BaseUserManager):

    # -----------CREATING THE USER---------
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("email address cannot be left empty!"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_type", 'ADMIN')
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("superuser must set is_staff to True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superuser must set is_superuser to True"))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    USER_TYPE_CHOICES = (
        ('ORGANIZATION', 'Organization'),
        ('MEMBER', 'Member'),
        ('ADMIN', 'Administrator')
    )

    username = None
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(
        _("first name"), max_length=150, blank=False, default="")
    last_name = models.CharField(
        _("last name"), max_length=150, blank=False,  default="")
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    user_type = models.CharField(
        choices=USER_TYPE_CHOICES, max_length=15, default="MEMBER")
    last_login = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # the organization this user is affiliated with is stored as unique_id---------------
    AffiliatedOrg = models.SlugField()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    # generate tokens for login
    def tokens(self):
        # create the tokens
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


# next tell django you are using this model for Authentication. do that in settings.py
