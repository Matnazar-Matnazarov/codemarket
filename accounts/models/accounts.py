from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from simple_history.models import HistoricalRecords

PHONE_REGEX = (
    r"^\+?1?\d{9,15}$|"
    r"^\+998\d{9}$|"
    r"^\+7\d{10}$|"
    r"^\+82\d{9,10}$|"
    r"^\+7\d{9,10}$|"
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                PHONE_REGEX, code="invalid", message="Enter a valid phone number"
            )
        ],
    )
    picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    objects = CustomUserManager()
    history = HistoricalRecords()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    #
    # @property
    # def __str__(self):
    #     return f"{self.email}"
