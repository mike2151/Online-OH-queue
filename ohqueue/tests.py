from django.test import TestCase
from .models import OHQueue
from freezegun import freeze_time
from users.models import StudentUser
import datetime
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
import json

class OHCreation(TestCase):
    def test_ohqueue_created(self):
        queue = OHQueue.objects.create(name="main", monday_times="4:00pm-6:00pm")
        self.assertEquals("main", queue.name)
        self.assertEquals("4:00pm-6:00pm", queue.monday_times)

# These tests assume New York Time zone!
class OHQuestions(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.queue = OHQueue.objects.create(name="main", monday_times="4:00pm-6:00pm")
        # monday time at queue opening time
        freezer = freeze_time("2018-12-31 21:00:01")
        freezer.start()

        self.student_user = StudentUser.objects.create(username="test", email="test@upenn.edu", first_name="tester", 
        last_name="smith", password="testing123")
        self.student_user.set_password("testing123")
        self.student_user.is_active = True
        self.student_user.save()

        self.student_user_two = StudentUser.objects.create(username="test2", email="test2@upenn.edu", first_name="tester2", 
        last_name="smith", password="testing123")
        self.student_user_two.set_password("testing123")
        self.student_user_two.is_active = True
        self.student_user_two.save()

        self.ta_user = StudentUser.objects.create(username="ta", email="ta@upenn.edu", first_name="ta", 
        last_name="smith", password="testing123")
        self.ta_user.set_password("testing123")
        self.ta_user.is_active = True
        self.ta_user.is_ta = True
        self.ta_user.save()

    def generate_header(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    def test_queue_is_open(self):
        self.generate_header(self.student_user)
        response = self.client.get('/api/v1/queue/list/')
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, len(json.loads(response.content)))

    def test_is_queue_open_unauthenticated(self):
        response = self.client.get('/api/v1/queue/list/')
        self.assertEquals(401, response.status_code)

    def test_queue_is_closed(self):
        freezer = freeze_time("2018-12-31 16:00:01")
        freezer.start()
        self.generate_header(self.student_user)
        response = self.client.get('/api/v1/queue/list/')
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, len(json.loads(response.content)))
    
    def test_get_queue_not_authenticated(self):
        response = self.client.get('/api/v1/queue/list/')
        self.assertEquals(401, response.status_code)

    # extend open tests

    def test_can_extend_ohqueue(self):
        self.generate_header(self.ta_user)
        response = self.client.post('/api/v1/queue/open/', {"queue": "main"}, format="json")
        self.assertTrue(json.loads(response.content)["success"])
    
    def test_student_cannot_extend_ohqueue(self):
        self.generate_header(self.student_user)
        response = self.client.post('/api/v1/queue/open/', {"queue": "main"}, format="json")
        self.assertFalse(json.loads(response.content)["success"])

    def test_unauthenticated_cannot_extend_ohqueue(self):
        response = self.client.post('/api/v1/queue/open/', {"queue": "main"}, format="json")
        self.assertFalse(json.loads(response.content)["success"])

    def test_closed_then_extended_open(self):
        freezer = freeze_time("2018-12-31 16:00:01")
        freezer.start()

        self.generate_header(self.student_user)
        response = self.client.get('/api/v1/queue/list/')
        self.assertEquals(0, len(json.loads(response.content)))

        self.generate_header(self.ta_user)
        response = self.client.post('/api/v1/queue/open/', {"queue": "main"}, format="json")
        self.assertTrue(json.loads(response.content)["success"])
        
        self.generate_header(self.student_user)
        response = self.client.get('/api/v1/queue/list/')
        self.assertEquals(1, len(json.loads(response.content)))
    
    # close early tests

    def test_can_close_ohqueue(self):
        self.generate_header(self.ta_user)
        response = self.client.post('/api/v1/queue/close/', {"queue": "main"}, format="json")
        self.assertTrue(json.loads(response.content)["success"])
    
    def test_student_cannot_close_ohqueue(self):
        self.generate_header(self.student_user)
        response = self.client.post('/api/v1/queue/close/', {"queue": "main"}, format="json")
        self.assertFalse(json.loads(response.content)["success"])

    def test_unauthenticated_cannot_close_ohqueue(self):
        response = self.client.post('/api/v1/queue/close/', {"queue": "main"}, format="json")
        self.assertFalse(json.loads(response.content)["success"])

    def test_open_then_closed(self):
        self.generate_header(self.student_user)
        response = self.client.get('/api/v1/queue/list/')
        self.assertEquals(1, len(json.loads(response.content)))

        self.generate_header(self.ta_user)
        response = self.client.post('/api/v1/queue/close/', {"queue": "main"}, format="json")
        self.assertTrue(json.loads(response.content)["success"])
        
        self.generate_header(self.student_user)
        response = self.client.get('/api/v1/queue/list/')
        self.assertEquals(0, len(json.loads(response.content)))

    # ask questions

    def test_anon_cant_ask_question(self):
        response = self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertIn("Authentication credentials were not provided.", json.loads(response.content)["detail"])
    
    def test_can_ask_question(self):
        self.generate_header(self.student_user)
        response = self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, len(self.queue.questions.values()))

    def test_student_cannot_ask_two_question(self):
        self.generate_header(self.student_user)
        response = self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, len(self.queue.questions.values()))

        response = self.client.post('/api/v1/queue/main/ask', {"description": "my question 2"}, format="json")
        self.assertEquals(400, response.status_code)
        self.assertEquals(1, len(self.queue.questions.values()))

    def test_student_cannot_ask_two_questions_in_dif_queues(self):

        queue_two = OHQueue.objects.create(name="second", monday_times="4:00pm-6:00pm")

        self.generate_header(self.student_user)
        response = self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, len(self.queue.questions.values()) + len(queue_two.questions.values()))

        response = self.client.post('/api/v1/queue/second/ask', {"description": "my question 2"}, format="json")
        self.assertEquals(400, response.status_code)
        self.assertEquals(1, len(self.queue.questions.values()) + len(queue_two.questions.values()))

    def test_two_students_can_ask_two_questions_same_queue(self):
        self.generate_header(self.student_user)
        response = self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, len(self.queue.questions.values()))

        self.generate_header(self.student_user_two)
        response = self.client.post('/api/v1/queue/main/ask', {"description": "my question 2"}, format="json")
        self.assertEquals(201, response.status_code)
        self.assertEquals(2, len(self.queue.questions.values()))

        self.assertEquals("my question", self.queue.questions.values()[0]["description"])
        self.assertEquals("my question 2", self.queue.questions.values()[1]["description"])

    def test_two_students_can_ask_two_questions_different_queue(self):
        queue_two = OHQueue.objects.create(name="second", monday_times="4:00pm-6:00pm")

        self.generate_header(self.student_user)
        response = self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, len(self.queue.questions.values()))

        self.generate_header(self.student_user_two)
        response = self.client.post('/api/v1/queue/second/ask', {"description": "my question 2"}, format="json")
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, len(queue_two.questions.values()))

        self.assertEquals("my question", self.queue.questions.values()[0]["description"])
        self.assertEquals("my question 2", queue_two.questions.values()[0]["description"])
        
    # answering questions

    def test_ta_can_answer_questions(self):
        self.generate_header(self.student_user)
        self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertEquals(1, len(self.queue.questions.values()))

        question_id_one = (self.queue.questions.values()[0]["id"])

        self.generate_header(self.ta_user)
        response = self.client.post('/api/v1/questions/answer/', 
        {"queue": "main", "question_id": question_id_one}, format="json")
        self.assertEquals(200, response.status_code)
        self.assertTrue(json.loads(response.content)["success"])
        self.assertEquals(0, len(self.queue.questions.values()))

    def test_anon_cannot_answer_questions(self):
        self.generate_header(self.student_user)
        self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")

        self.client.credentials()
        response = self.client.post('/api/v1/questions/answer/', 
        {"queue": "main", "question_id": 1}, format="json")
        self.assertFalse(json.loads(response.content)["success"])
        self.assertEquals(1, len(self.queue.questions.values()))

    def test_student_cannot_answer_questions(self):
        self.generate_header(self.student_user)
        self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")

        self.generate_header(self.student_user_two)
        response = self.client.post('/api/v1/questions/answer/', 
        {"queue": "main", "question_id": 1}, format="json")
        self.assertFalse(json.loads(response.content)["success"])
        self.assertEquals(1, len(self.queue.questions.values()))

    def test_ta_answer_queue_of_two_questions(self):
        self.generate_header(self.student_user)
        response = self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")

        self.generate_header(self.student_user_two)
        response = self.client.post('/api/v1/queue/main/ask', {"description": "my question 2"}, format="json")
        
        question_id_one = (self.queue.questions.values()[0]["id"])

        self.generate_header(self.ta_user)
        response = self.client.post('/api/v1/questions/answer/', 
        {"queue": "main", "question_id": question_id_one}, format="json")
        
        self.assertEquals("my question 2", self.queue.questions.values()[0]["description"])
        self.assertEquals(1, len(self.queue.questions.values()))

        question_id_two = (self.queue.questions.values()[0]["id"])

        self.generate_header(self.ta_user)
        response = self.client.post('/api/v1/questions/answer/', 
        {"queue": "main", "question_id": question_id_two}, format="json")

        self.assertEquals(0, len(self.queue.questions.values()))

    def test_ta_cannot_answer_not_valid_queue(self):
        self.generate_header(self.student_user)
        self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertEquals(1, len(self.queue.questions.values()))

        self.generate_header(self.ta_user)
        response = self.client.post('/api/v1/questions/answer/', 
        {"queue": "random", "question_id": 1}, format="json")
        self.assertFalse(json.loads(response.content)["success"])
        self.assertEquals(1, len(self.queue.questions.values()))

    def test_ta_cannot_answer_not_valid_question_id(self):
        self.generate_header(self.student_user)
        self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertEquals(1, len(self.queue.questions.values()))

        self.generate_header(self.ta_user)
        response = self.client.post('/api/v1/questions/answer/', 
        {"queue": "main", "question_id": 15}, format="json")
        self.assertFalse(json.loads(response.content)["success"])
        self.assertEquals(1, len(self.queue.questions.values()))

    # edit questions
    def test_can_edit_question(self):
        self.generate_header(self.student_user)
        self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertEquals("my question", self.queue.questions.values()[0]["description"])

        question_id = str(self.queue.questions.values()[0]["id"])

        response = self.client.put('/api/v1/queue/question/' + question_id + '/edit',
         {"description": "new question"}, format="json")
        self.assertTrue(json.loads(response.content)["success"])
        self.assertEquals("new question", self.queue.questions.values()[0]["description"])

    def test_anon_cannot_edit_question(self):
        self.generate_header(self.student_user)
        self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertEquals("my question", self.queue.questions.values()[0]["description"])

        question_id = str(self.queue.questions.values()[0]["id"])
        
        self.client.credentials()
        response = self.client.put('/api/v1/queue/question/' + question_id +'/edit', {"description": "new question"}, format="json")
        self.assertTrue(401, response.status_code)
        self.assertEquals("my question", self.queue.questions.values()[0]["description"])

    def test_other_student_cannot_edit(self):
        self.generate_header(self.student_user)
        self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertEquals("my question", self.queue.questions.values()[0]["description"])

        question_id = str(self.queue.questions.values()[0]["id"])
        
        self.generate_header(self.student_user_two)
        response = self.client.put('/api/v1/queue/question/' + question_id + '/edit', {"description": "new question"}, format="json")
        self.assertFalse(json.loads(response.content)["success"])
        self.assertEquals("my question", self.queue.questions.values()[0]["description"])

    def test_edit_non_existent_question(self):
        self.generate_header(self.student_user)
        response = self.client.put('/api/v1/queue/question/15/edit', {"description": "new question"}, format="json")
        self.assertFalse(json.loads(response.content)["success"])
    
    # delete questions
    def test_user_can_delete_question(self):
        self.generate_header(self.student_user)
        self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertEquals(1, len(self.queue.questions.values()))

        question_id = self.queue.questions.values()[0]["id"]
        
        response = self.client.post('/api/v1/questions/delete/', {"question_id": question_id}, format="json")
        self.assertTrue(json.loads(response.content)["success"])
        self.assertEquals(0, len(self.queue.questions.values()))
    
    def test_anon_cannot_delete_question(self):
        self.generate_header(self.student_user)
        self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertEquals(1, len(self.queue.questions.values()))

        question_id = self.queue.questions.values()[0]["id"]
        
        self.client.credentials()
        response = self.client.post('/api/v1/questions/delete/', {"question_id": question_id}, format="json")
        self.assertFalse(json.loads(response.content)["success"])
        self.assertEquals(1, len(self.queue.questions.values()))
    
    def test_other_user_cannot_delete_question(self):
        self.generate_header(self.student_user)
        self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")
        self.assertEquals(1, len(self.queue.questions.values()))

        question_id = self.queue.questions.values()[0]["id"]
        
        self.generate_header(self.student_user_two)
        response = self.client.post('/api/v1/questions/delete/', {"question_id": question_id}, format="json")
        self.assertFalse(json.loads(response.content)["success"])
        self.assertEquals(1, len(self.queue.questions.values()))
    
    def test_delete_with_multiple_questions(self):
        self.generate_header(self.student_user)
        response = self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")

        self.generate_header(self.student_user_two)
        response = self.client.post('/api/v1/queue/main/ask', {"description": "my question 2"}, format="json")
        self.assertEquals(2, len(self.queue.questions.values()))

        question_id = self.queue.questions.values()[0]["id"]

        self.generate_header(self.student_user)
        response = self.client.post('/api/v1/questions/delete/', {"question_id": question_id}, format="json")
        self.assertEquals(1, len(self.queue.questions.values()))

        self.assertEquals("my question 2", self.queue.questions.values()[0]["description"])