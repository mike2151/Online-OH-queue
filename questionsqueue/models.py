from django.db import models
from users.models import StudentUser
class Question(models.Model):
    author = models.OneToOneField(StudentUser, on_delete=models.CASCADE, related_name="student")    
    answered_by = models.OneToOneField(StudentUser, on_delete=models.CASCADE, related_name="TA")   
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=280)
    ask_date = models.DateTimeField(auto_now_add=True)
