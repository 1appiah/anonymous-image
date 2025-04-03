from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
# Create your models here.


class NewUser(AbstractUser,PermissionsMixin):
    email = models.EmailField(("email address"), unique=True)
    username = models.CharField (max_length=150,unique=True)
    first_name = models.CharField (max_length=150)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name']

    def __str__(self) -> str:
        return self.username
    

