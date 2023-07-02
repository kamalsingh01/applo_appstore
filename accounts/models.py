from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils.translation import gettext_lazy as _

class UserRoles(models.Choices):
    ADMIN = 'admin'
    USER = 'user'

# Custom User Model
class UserModel(AbstractUser):
    objects = UserManager()

    id = models.AutoField(_("Unique identifier for user"), primary_key=True, editable=False)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(_("username"), unique=True, null=False)
    phone_number = models.CharField(max_length=15, null=True, unique=True)
    user_role = models.CharField(max_length=5, default='user', blank=True)
    app_points = models.IntegerField(default=0)
    profile_image = models.ImageField(upload_to="user/", null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "email",
    ]

    class Meta:
        db_table = "user_table"
