from django.db import models
from questions.models import Question

# Create your models here.
class OHQueue(models.Model):
    name = models.CharField(max_length=256, unique=True)
    questions = models.ManyToManyField(Question, blank=True)
    times_open = models.CharField(max_length=1024)
    average_wait_time = models.FloatField(default=0.0)

    def question_contents(self):
        question_content = []
        for question in self.questions.all():
            question_dict = {
                "first_name": question.author_first_name, 
                "last_name": question.author_last_name,
                "email": question.author_email,
                "question_content": question.description,
                "id": question.id,
            }
            question_content.append(question_dict)
        return question_content

    def ask_question(self):
        pass
    
    def answer_question(self):
        pass

    def __str__(self):
        return self.name