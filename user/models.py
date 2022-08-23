from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)
    phone = models.CharField(blank=True, null = True,unique=True,max_length=13)
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()