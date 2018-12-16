from django.contrib.auth.models import AbstractUser
from django.db import models

class StudentUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Penn Email Address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        pennkey = self.email.split("@")[0]
        return pennkey