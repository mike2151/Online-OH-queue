from django.db import models
from users.models import StudentUser
class Question(models.Model):
    author_email = models.CharField(max_length=512, default='No Account')    
    author_first_name = models.CharField(max_length=512, default='No first name')    
    author_last_name = models.CharField(max_length=512, default='No last name')
    answered_by_email = models.CharField(max_length=512, default='No Account') 
    is_answered = models.BooleanField(default=False)
    description = models.CharField(max_length=280)
    ask_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description