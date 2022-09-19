from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
import csv
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
city_values = []
state_values = []
country_values = [("INDIA", "India")]
with open("datafiles/city-state.csv", encoding="utf-8") as cityfile:
    csvreader = csv.reader(cityfile)
    header = next(csvreader)
    for row in csvreader:
        city_values.append(tuple((row[0], row[0])))
        state_values.append(tuple((row[-1], row[-1])))


def get_city_values():
    return city_values


def get_state_values():
    return state_values
def get_country_values():
    return country_values

class CustomerManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):

        if username and email:

            email = self.normalize_email(email)
            username = str(username)
            user = self.model(
                username=username, email=email, password=password,**extra_fields
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
        else:
            raise ValueError("Username & Email must be set")

    def create_user(self, username, email, password, **extra_fields):

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(username, email, password, **extra_fields)


class Customer(AbstractUser):
    username = models.CharField(
        _("Name"),
        max_length=50,
    )
    email = models.EmailField(_("email address"), unique=True, max_length=50)

    address1 = models.TextField(_("Address Line 1"), null=True, max_length=255)

    address2 = models.TextField(_("Address Line 2"), blank=True, max_length=255)

    phone = PhoneNumberField(null=True)

    
    country = models.CharField(
        _("country"),
        choices=country_values,
        max_length=5,
        null=True,
    )

    STATES = state_values

    state = models.CharField(_("state"), choices=STATES, max_length=30, null=True)

    CITIES = city_values

    city = models.CharField(_("city"), choices=CITIES, max_length=30, null=True)

    objects = CustomerManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
