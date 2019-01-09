from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

class StudentUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Penn Email Address',
        max_length=64,
        unique=True,
    )
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    is_ta = models.BooleanField(default=False, verbose_name="Teaching Assistant")

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        pennkey = self.email.split("@")[0]
        return pennkey

    def save(self, *args, **kwargs):
       if self.is_superuser:
           self.is_ta = True
           self.is_staff = True
       else:
           self.is_staff = False
       return super(StudentUser, self).save(*args, **kwargs)
