from django.test import override_settings
from rest_framework.test import APITestCase, APIClient


class ThrottleApiTests(APITestCase):
    # make sure to override your settings for testing
    TESTING_THRESHOLD = 50
    def test_check_login_api_throttle(self):
        client = APIClient()
        # this is probably set in settings in you case
        for i in range(0, self.TESTING_THRESHOLD):
            client.post("/api/v1/users/login/", {"email": "wrong@upenn.edu", "password": "wrong"}, format="json")

        response = client.post("/api/v1/users/login/", {"email": "wrong@upenn.edu", "password": "wrong"}, format="json")
        # 429 - too many requests
        self.assertEqual(response.status_code, 429)
    
    def test_check_register_api_throttle(self):
        client = APIClient()
        # this is probably set in settings in you case
        for i in range(0, self.TESTING_THRESHOLD):
            client.post("/api/v1/users/register/", 
            {"email": "wrong@upenn.edu", "first_name": "mike" , "last_name": "yo" ,"password": "wrong"},
             format="json")

        response = client.post("/api/v1/users/register/", 
            {"email": "wrong@upenn.edu", "first_name": "mike" , "last_name": "yo" ,"password": "wrong"},
             format="json")
         # 429 - too many requests
        self.assertEqual(response.status_code, 429)