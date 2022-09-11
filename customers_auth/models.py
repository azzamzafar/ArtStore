
from django.db import models
from django.contrib.auth.models import AbstratctUser,UserManager
from django.utils.translation import gettext_lazy as _
import csv
# Create your models here.

city_values = []
state_values = []
with open("city-state.csv",encoding="utf-8") as cityfile:
    csvreader = csv.reader(cityfile)
    header = next(csvreader)
    for row in csvreader:
        city_values.append(
            tuple((row[0],row[0]))
            )
        state_values.append(
            tuple((row[-1],row[-1]))
        )
def get_city_values():
    return city_values
def get_state_values():
    return state_values

class CustomerManager(UserManager):
    def _create_user(self,username,email,password,**extra_fields):
        if not username and email:
            raise ValueError("Username & Email must be set")
        email = self.normalize_email(email)
        
        user = self.model(username=username,email=email,**extra_fields)
    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        
    ...

class Customer(AbstratctUser):
    username = models.CharField(
        _("Name"),
        max_length=50,
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        max_length=50)
    
    COUNTRIES = ['India']
    
    country = models.CharField(
        _("country"),
        choices = COUNTRIES,
        Null=True,
    )
    phone = ...
    STATES = state_values
    state = models.CharField(
        _("state"),
        choices=STATES,
        max_length=10,
        Null=True
    )
    CITIES = city_values
    city = models.CharField(
        _("state"),
        choices = CITIES,
        max_length=20,
        Null=True
    )
    address1 = models.TextField(
        _("Address Line 1"),
        Null=True,
        max_length=255
    )
    address2 = models.TextField(
        _("Address Line 2"),
        Blank=True,
        max_length=255
    )
    
    objects = CustomerManager()
    
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username","email"]

    
