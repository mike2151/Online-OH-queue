from django.test import TestCase
from .models import StudentUser

class UserCreationTest(TestCase):
    def setUp(self):
        StudentUser.objects.create(email="test@upenn.edu", first_name="tester", last_name="smith", password="yodogyoo")

    def test_user_is_created(self):
        user = StudentUser.objects.get(email="test@upenn.edu")
        self.assertFalse(user.is_ta)
        self.assertEqual(user.first_name, "tester")
