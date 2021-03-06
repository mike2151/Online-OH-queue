from django.test import TestCase
from .models import StudentUser
from rest_framework.test import APIClient
import json
from rest_framework import status
from django.core import mail

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
    def setUp(self):
        client = APIClient()

    def test_incomplete(self):
        response = self.client.post('/api/v1/users/register/', {'email': 'mike@upenn.com',
          "last_name": "smith", "password": "passdogyo"}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertIn("This field is required.", ((json.loads(response.content))["first_name"]))
        
    def test_no_penn_email(self):
        response = self.client.post('/api/v1/users/register/', {'email': 'mike@gmail.com',
         "first_name": "mike", "last_name": "smith", "password": "passdogyo"}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertIn("Email is not a Penn Email", ((json.loads(response.content))["email"]))

    def test_plus_in_email(self):
        response = self.client.post('/api/v1/users/register/', {'email': 'mike+2@upenn.edu',
         "first_name": "mike", "last_name": "smith", "password": "passdogyo"}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertIn("No special characters allowed", ((json.loads(response.content))["email"]))
    
    def test_successful_creation(self):
        response = self.client.post('/api/v1/users/register/', {"email": "mike@upenn.edu", "first_name": "mike", "last_name": "smith", "password": "passdogyo"}, format='json')
        self.assertEqual(201, response.status_code)

    def test_pass_too_short(self):
        response = self.client.post('/api/v1/users/register/', {'email': 'mike@upenn.edu',
         "first_name": "mike", "last_name": "smith", "password": "1"}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertIn("Password too short. Should be at least 8 characters.", ((json.loads(response.content))["password"]))

    def test_account_already_made(self):   
        StudentUser.objects.create(email="test@upenn.edu", first_name="tester", last_name="smith", password="yodogyoo")
        test_user = StudentUser.objects.get(email="test@upenn.edu")
        self.assertTrue(test_user.is_active)
        response = self.client.post('/api/v1/users/register/', {'email': 'test@upenn.edu',
         "first_name": "mike", "last_name": "smith", "password": "1"}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertIn("user with this Penn Email Address already exists.", ((json.loads(response.content))["email"]))

    def test_cannot_login_until_activated(self):
        self.client.post('/api/v1/users/register/', {"email": "test@upenn.edu", "first_name": "mike", 
        "last_name": "hello", "password": "testing123"}, format='json')

        response = self.client.post('/api/v1/users/login/', 
        {"email": "test@upenn.edu", "password": "testing123"}, format='json')
        self.assertEquals(404, response.status_code)

class EmailRegistrationTest(TestCase):
    def setUp(self):
        client = APIClient()

    def test_email_sent_registration(self):
        self.client.post('/api/v1/users/register/', {"email": "mike@upenn.edu", 
        "first_name": "mike", "last_name": "smith", "password": "passdogyo"}, format='json')
        self.assertEqual(len(mail.outbox), 1)
    def test_confirmed_emailed_twice(self):
        self.client.post('/api/v1/users/register/', {"email": "mike@upenn.edu", 
        "first_name": "imposter", "last_name": "smith", "password": "passdogyo"}, format='json')
        self.assertEqual(len(mail.outbox), 1)
        self.client.post('/api/v1/users/register/', {"email": "mike@upenn.edu", 
        "first_name": "mike", "last_name": "smith", "password": "diffpassdogyo"}, format='json')
        self.assertEqual(len(mail.outbox), 2)
    def test_trying_to_reg_already_reg_user(self):
        StudentUser.objects.create(email="test@upenn.edu", first_name="tester", last_name="smith", password="yodogyoo")
        self.client.post('/api/v1/users/register/', {"email": "test@upenn.edu", 
        "first_name": "mike", "last_name": "smith", "password": "diffpassdogyo"}, format='json')
        self.assertEqual(len(mail.outbox), 0)
        

class LoginTests(TestCase):
    def setUp(self):
        client = APIClient()
        user = StudentUser.objects.create(email="test@upenn.edu", first_name="tester", last_name="smith", password="testing123")
        user.set_password("testing123")
        user.is_active = True
        user.save()

    def test_valid_login(self):
        response = self.client.post('/api/v1/users/login/', 
        {"email": "test@upenn.edu", "password": "testing123"}, format='json')
        self.assertEquals(200, response.status_code)

    def test_missing_field_login(self):
        response = self.client.post('/api/v1/users/login/', 
        {"email": "test@upenn.edu"}, format='json')
        self.assertEquals(400, response.status_code)

    def test_user_does_not_exist(self):
        response = self.client.post('/api/v1/users/login/', 
        {"email": "bill@upenn.edu", "password": "testing123"}, format='json')
        self.assertEquals(404, response.status_code)

        