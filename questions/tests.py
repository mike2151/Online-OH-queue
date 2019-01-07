from django.test import TestCase
from .models import Question

class QuestionCreation(TestCase):     
    def test_can_make_normal_question(self):
        question = Question.objects.create(author_email="test@upenn.edu", author_first_name="tester", 
        author_last_name="smith", answered_by_email="ta@upenn.edu", description="question")
        self.assertEquals("test@upenn.edu", question.author_email)
        self.assertEquals("tester", question.author_first_name)
        self.assertEquals("smith", question.author_last_name)
        self.assertEquals("ta@upenn.edu", question.answered_by_email)
        self.assertEquals("question", question.description)

