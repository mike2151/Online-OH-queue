from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import StudentUser
from questions.models import Question

class Feedback(models.Model):
    # 1 being too little help 10 more help
    helpful_scale = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ], blank=True, null=True)
    was_helpful = models.BooleanField(default=False, blank=False)
    comments = models.CharField(max_length=280, blank=True)
    feedback_time = models.DateTimeField(auto_now_add=True)
    ta_email = models.CharField(max_length=64, default='No Account')
    base_question = models.ForeignKey(Question, unique=True, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.ta_email + " : " + str(self.feedback_time)
