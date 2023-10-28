# from django.db import models
from django_softdelete.models import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from organisations.managers.user_manager import UserManager


# Create your models here.

class Country(models.Model):
    # id = models.BigAutoField()
    continent = models.CharField(
        max_length=20,
        choices=[
            ("Af", "Afrique"),
            ("Eu", "Europe"),
            ("Asie", "Asie"),
            ("Amerique", "Amerique"),
            ("Oceanie", "Oceanie"),
        ],
        default="Af"
    )
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)

    @property
    def to_json(self):
        return {
            "continent": self.continent,
            "name": self.name
        }


class Organisations(models.Model):
    # id = models.BigAutoField()
    name = models.CharField(max_length=100, null=False, unique=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    cover = models.ImageField(upload_to="uploads/organisations", null=True, blank=True)
    email = models.EmailField(unique=True)

    @property
    def to_json(self):
        return {
            "name": self.name,
            "country": self.country.id,
            "address": self.address,
            "cover": self.cover,
            "email": self.email
        }


class User(AbstractBaseUser):
    # id = models.BigAutoField()
    username = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(upload_to="uploads/avatars", null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250, blank=False, null=False)
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    account_type = models.CharField(
        max_length=20,
        choices=[
            ("admin", "admin"),
            ("super admin", "super admin")
        ]
    )

    objects = UserManager()

    USERNAME_FIELD = "username"

    @property
    def is_super_admin(self):
        if self.account_type == "admin":
            return False
        elif self.account_type == "super admin":
            return True

    @property
    def to_json(self):
        return {
            "username": self.username,
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "avatar": self.avatar,
            "organisation": self.organisation.id,
            "is_active": self.is_active,
            "account_type": self.account_type
        }
