from django.test import TestCase
import json
from users.models import StudentUser
from rest_framework.test import  APIClient
from rest_framework.authtoken.models import Token

class PermissionsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.ta_user = StudentUser.objects.create(username="ta", email="ta@upenn.edu", first_name="ta", 
        last_name="smith", password="testing123")
        self.ta_user.set_password("testing123")
        self.ta_user.is_active = True
        self.ta_user.is_ta = True
        self.ta_user.save()

        self.student_user = StudentUser.objects.create(username="test", email="test@upenn.edu", first_name="tester", 
        last_name="smith", password="testing123")
        self.student_user.set_password("testing123")
        self.student_user.is_active = True
        self.student_user.save()

        self.admin_user = StudentUser.objects.create_superuser(username="admin", email="admin@upenn.edu", first_name="admin", 
        last_name="smith", password="testing123")
        self.admin_user.set_password("testing123")
        self.admin_user.is_active = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

    def generate_header(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    # asker tests

    def test_anon_cannot_access_frequent_asker(self):
        response = self.client.get('/api/v1/stats/frequentasker/')
        self.assertFalse(json.loads(response.content)["authenticated"])

    def test_student_cannot_access_frequent_asker(self):
        self.generate_header(self.student_user)
        response = self.client.get('/api/v1/stats/frequentasker/')
        self.assertFalse(json.loads(response.content)["authenticated"])
    
    def test_ta_cannot_access_frequent_asker(self):
        self.generate_header(self.ta_user)
        response = self.client.get('/api/v1/stats/frequentasker/')
        self.assertFalse(json.loads(response.content)["authenticated"])

    def test_admin_can_access_frequent_asker(self):
        self.generate_header(self.admin_user)
        response = self.client.get('/api/v1/stats/frequentasker/')
        self.assertTrue(json.loads(response.content)["authenticated"])

    # answerer tests

    def test_anon_cannot_access_frequent_answer(self):
        response = self.client.get('/api/v1/stats/frequentanswer/')
        self.assertFalse(json.loads(response.content)["authenticated"])

    def test_student_cannot_access_frequent_answer(self):
        self.generate_header(self.student_user)
        response = self.client.get('/api/v1/stats/frequentanswer/')
        self.assertFalse(json.loads(response.content)["authenticated"])
    
    def test_ta_cannot_access_frequent_answer(self):
        self.generate_header(self.ta_user)
        response = self.client.get('/api/v1/stats/frequentanswer/')
        self.assertFalse(json.loads(response.content)["authenticated"])

    def test_admin_can_access_frequent_answer(self):
        self.generate_header(self.admin_user)
        response = self.client.get('/api/v1/stats/frequentanswer/')
        self.assertTrue(json.loads(response.content)["authenticated"])

    # summary tests
    def test_anon_cannot_access_summary(self):
        response = self.client.get('/api/v1/summary/')
        self.assertEquals(401, response.status_code)

    def test_student_cannot_access_summary(self):
        self.generate_header(self.student_user)
        response = self.client.get('/api/v1/summary/')
        self.assertNotEqual(200, response.status_code)
    
    def test_ta_can_access_summary(self):
        self.generate_header(self.ta_user)
        response = self.client.get('/api/v1/summary/')
        self.assertEquals(200, response.status_code)