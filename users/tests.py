from django.test import TestCase
from .models import StudentUser
from rest_framework.test import APIClient
import json
from rest_framework import status

class UserCreationTest(TestCase):
    def setUp(self):
        StudentUser.objects.create(email="test@upenn.edu", first_name="tester", last_name="smith", password="yodogyoo")

    def test_user_is_created(self):
        user = StudentUser.objects.get(email="test@upenn.edu")
        self.assertFalse(user.is_ta)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.first_name, "tester")
        self.assertEqual(user.last_name, "smith")
    
    def test_user_promoted_to_ta_when_admin(self):
        user = StudentUser.objects.get(email="test@upenn.edu")
        user.is_superuser = True
        user.save()
        self.assertTrue(user.is_ta)

class UserRegistrationTest(TestCase):
    def test_incomplete(self):
        client = APIClient()
        response = client.post('/api/v1/users/register/', {'email': 'mike@upenn.com',
          "last_name": "smith", "password": "passdogyo"}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertIn("This field is required.", ((json.loads(response.content))["first_name"]))
        
    def test_no_penn_email(self):
        client = APIClient()
        response = client.post('/api/v1/users/register/', {'email': 'mike@gmail.com',
         "first_name": "mike", "last_name": "smith", "password": "passdogyo"}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertIn("Email is not a Penn Email", ((json.loads(response.content))["email"]))
    
    def test_successful_creation(self):
        client = APIClient()
        response = client.post('/api/v1/users/register/', {"email": "mike@upenn.edu", "first_name": "mike", "last_name": "smith", "password": "passdogyo"}, format='json')
        self.assertEqual(201, response.status_code)

    def test_pass_too_short(self):
        client = APIClient()
        response = client.post('/api/v1/users/register/', {'email': 'mike@upenn.edu',
         "first_name": "mike", "last_name": "smith", "password": "1"}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertIn("Password too short. Should be at least 8 characters.", ((json.loads(response.content))["password"]))

    def test_account_already_made(self):   
        client = APIClient()
        StudentUser.objects.create(email="test@upenn.edu", first_name="tester", last_name="smith", password="yodogyoo")
        test_user = StudentUser.objects.get(email="test@upenn.edu")
        self.assertTrue(test_user.is_active)
        response = client.post('/api/v1/users/register/', {'email': 'test@upenn.edu',
         "first_name": "mike", "last_name": "smith", "password": "1"}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertIn("user with this Penn Email Address already exists.", ((json.loads(response.content))["email"]))

    