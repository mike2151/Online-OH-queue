from django.db import models
from users.models import StudentUser
class Question(models.Model):
    author_email = models.CharField(max_length=512, default='No Account')    
    answered_by_email = models.CharField(max_length=512, default='No Account') 
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=280)
    ask_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description