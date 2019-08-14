from django.db import models
from users.models import StudentUser

class Question(models.Model):
    author_email = models.CharField(max_length=64, default='No Account')    
    author_first_name = models.CharField(max_length=32, default='No first name')    
    author_last_name = models.CharField(max_length=32, default='No last name')
    answered_by_email = models.CharField(max_length=64, default='No Account') 
    answerer_first_name = models.CharField(max_length=32, default='') 
    answerer_last_name = models.CharField(max_length=32, default='') 
    is_answered = models.BooleanField(default=False)
    description = models.CharField(max_length=280)
    ask_date = models.DateTimeField(auto_now_add=True)
    host_queue = models.CharField(max_length=32, default='')
    feedback_for_q = models.ForeignKey('feedback.Feedback', unique=True, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.description
