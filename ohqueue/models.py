from django.db import models
from questions.models import Question

# Create your models here.
class OHQueue(models.Model):
    name = models.CharField(max_length=256)
    questions = models.ManyToManyField(Question)
    times_open = models.CharField(max_length=1024)
    average_wait_time = models.FloatField(default=0.0)

    def ask_question(self):
        pass
    
    def answer_question(self):
        pass

    def __str__(self):
        return self.name