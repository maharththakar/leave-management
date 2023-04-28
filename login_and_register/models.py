from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_faculty= models.BooleanField('Is faculty', default=False)
    is_ta = models.BooleanField('Is ta', default=False)
    is_student = models.BooleanField('Is student', default=False)
