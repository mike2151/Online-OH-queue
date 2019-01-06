from django.test import TestCase
from .models import OHQueue
from freezegun import freeze_time
from users.models import StudentUser
import datetime
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
import json
import string, random

class OHCreation(TestCase):
    def setUp(self):
        self.queue = OHQueue.objects.create(name="main", monday_times="4:00pm-6:00pm")
        self.student_user = StudentUser.objects.create(username="test", email="test@upenn.edu", first_name="tester", 
        last_name="smith", password="testing123")
        self.student_user.set_password("testing123")
        self.student_user.is_active = True
        self.student_user.save()

    @freeze_time("2018-12-31 21:00:01")
    def test_ohqueue_created(self):
        self.assertEquals("main", self.queue.name)
        self.assertEquals("4:00pm-6:00pm", self.queue.monday_times)
        self.assertTrue(self.queue.isQueueActive(self.student_user))
    
    @freeze_time("2018-12-31 16:00:01")
    def test_is_queue_inactive(self):
        self.assertFalse(self.queue.isQueueActive(self.student_user))

    @freeze_time("2018-12-31 21:00:01")
    def test_update_time(self):
        self.assertTrue(self.queue.isQueueActive(self.student_user))
        freezer = freeze_time("2018-12-31 16:00:01")
        freezer.start()
        self.queue.updateTime()
        self.assertFalse(self.queue.is_in_time)
        
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
    

    # ta_list end point
    def test_queue_is_open_ta(self):
        self.generate_header(self.ta_user)
        response = self.client.get('/api/v1/queue/list_ta/')
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, len(json.loads(response.content)))

    def test_is_queue_open_unauthenticated_ta(self):
        response = self.client.get('/api/v1/queue/list_ta/')
        self.assertEquals(401, response.status_code)

    def test_is_queue_open_student_ta(self):
        response = self.client.get('/api/v1/queue/list_ta/')
        self.assertEquals(401, response.status_code)

    def test_queue_is_not_closed_ta(self):
        freezer = freeze_time("2018-12-31 16:00:01")
        freezer.start()
        self.generate_header(self.ta_user)
        response = self.client.get('/api/v1/queue/list_ta/')
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, len(json.loads(response.content)))
    

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

    def test_queue_is_open_if_student_still_has_question(self):
        self.generate_header(self.student_user)
        response = self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")

        self.generate_header(self.ta_user)
        response = self.client.post('/api/v1/queue/close/', {"queue": "main"}, format="json")

        self.generate_header(self.student_user)
        response = self.client.get('/api/v1/queue/list/')
        self.assertEquals(1, len(json.loads(response.content)))

        self.generate_header(self.student_user_two)
        response = self.client.get('/api/v1/queue/list/')
        self.assertEquals(0, len(json.loads(response.content)))

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

class LoadHandlingTests(TestCase):
    @freeze_time("2018-12-31 21:00:01", tick=True)
    def setUp(self):
        self.client = APIClient()
        
        self.queue = OHQueue.objects.create(name="main", monday_times="4:00pm-6:00pm")

        for i in range(50):
            self.new_student_ask_question()
       

    def gen_random_string(self, l):
        return ''.join(random.choice(string.ascii_lowercase) for x in range(l))    

    def generate_header(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    def new_student_ask_question(self):
        username = self.gen_random_string(8)
        first_name = self.gen_random_string(8)
        last_name = self.gen_random_string(8)
        password = self.gen_random_string(10)
        student_user = StudentUser.objects.create(
            username=username,
            email= username + "@upenn.edu", 
            first_name=first_name, 
            last_name=last_name, 
            password=password
        )
        student_user.set_password(password)
        student_user.is_active = True
        student_user.save()
        self.generate_header(student_user)
        self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")

    @freeze_time("2018-12-31 21:00:01", tick=True)
    def test_queue_can_handle_lot_of_questions(self):
        self.assertEquals(50, len(self.queue.questions.values()))
    
    @freeze_time("2018-12-31 21:00:01", tick=True)
    def test_queue_maintains_order(self):
        prev_question = None
        for question in self.queue.questions.values():
            if prev_question != None:
                self.assertTrue(question["ask_date"] > prev_question["ask_date"])
            prev_question = question

class AverageWaitTimeTesting(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.queue = OHQueue.objects.create(name="main", monday_times="4:00pm-6:00pm")

        self.ta_user = StudentUser.objects.create(username="ta", email="ta@upenn.edu", first_name="ta", 
        last_name="smith", password="testing123")
        self.ta_user.set_password("testing123")
        self.ta_user.is_active = True
        self.ta_user.is_ta = True
        self.ta_user.save()

        self.freezer = freeze_time("2018-12-31 21:00:01")
        self.freezer.start()

    def gen_random_string(self, l):
        return ''.join(random.choice(string.ascii_lowercase) for x in range(l))    

    def generate_header(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    def new_student_ask_question(self):
        username = self.gen_random_string(8)
        first_name = self.gen_random_string(8)
        last_name = self.gen_random_string(8)
        password = self.gen_random_string(10)
        student_user = StudentUser.objects.create(
            username=username,
            email= username + "@upenn.edu", 
            first_name=first_name, 
            last_name=last_name, 
            password=password
        )
        student_user.set_password(password)
        student_user.is_active = True
        student_user.save()
        self.generate_header(student_user)
        self.client.post('/api/v1/queue/main/ask', {"description": "my question"}, format="json")

    def answer_top_question(self):
        question_id_one = (self.queue.questions.values()[0]["id"])

        self.generate_header(self.ta_user)
        self.client.post('/api/v1/questions/answer/', 
        {"queue": "main", "question_id": question_id_one}, format="json")
    
    def test_wait_time_is_init_zero(self):
        self.assertEquals(0, self.queue.average_wait_time)
    
    def test_one_question_wait_time_is_zero(self):
        self.new_student_ask_question()
        self.freezer.stop()
        self.freezer = freeze_time("2018-12-31 21:01:01")
        self.freezer.start()
        self.answer_top_question()
        self.queue = OHQueue.objects.get(name="main")
        self.assertEquals(0, self.queue.average_wait_time)
    
    def test_two_question_wait_time_is_one(self):
        self.new_student_ask_question()
        self.freezer = freeze_time("2018-12-31 21:01:01")
        self.freezer.start()
        self.answer_top_question()

        self.new_student_ask_question()
        self.freezer = freeze_time("2018-12-31 21:02:01")
        self.freezer.start()
        self.answer_top_question()

        self.queue = OHQueue.objects.get(name="main")

        self.assertEquals(.5, self.queue.average_wait_time)

    def test_three_question_wait_time_is_one(self):
        self.new_student_ask_question()
        self.freezer = freeze_time("2018-12-31 21:01:01")
        self.freezer.start()
        self.answer_top_question()

        self.new_student_ask_question()
        self.freezer = freeze_time("2018-12-31 21:02:01")
        self.freezer.start()
        self.answer_top_question()

        self.new_student_ask_question()
        self.freezer = freeze_time("2018-12-31 21:04:01")
        self.freezer.start()
        self.answer_top_question()

        self.queue = OHQueue.objects.get(name="main")

        self.assertEquals(1, self.queue.average_wait_time)

    def test_four_question_wait_time_is_one(self):
        self.new_student_ask_question()
        self.freezer = freeze_time("2018-12-31 21:01:01")
        self.freezer.start()
        self.answer_top_question()

        self.new_student_ask_question()
        self.freezer = freeze_time("2018-12-31 21:02:01")
        self.freezer.start()
        self.answer_top_question()

        self.new_student_ask_question()
        self.freezer = freeze_time("2018-12-31 21:04:01")
        self.freezer.start()
        self.answer_top_question()

        self.new_student_ask_question()
        self.freezer = freeze_time("2018-12-31 21:14:01")
        self.freezer.start()
        self.answer_top_question()

        self.queue = OHQueue.objects.get(name="main")

        self.assertEquals(3.2, self.queue.average_wait_time)

    def test_after_one_hour_average_reset(self):
        self.new_student_ask_question()
        self.freezer = freeze_time("2018-12-31 21:01:01")
        self.freezer.start()
        self.answer_top_question()

        self.new_student_ask_question()
        self.freezer = freeze_time("2018-12-31 21:02:01")
        self.freezer.start()
        self.answer_top_question()

        self.queue = OHQueue.objects.get(name="main")

        self.assertEquals(.5, self.queue.average_wait_time)

        self.new_student_ask_question()
        self.freezer = freeze_time("2018-12-31 22:04:01")
        self.freezer.start()
        self.answer_top_question()

        self.queue = OHQueue.objects.get(name="main")

        self.assertEquals(0, self.queue.average_wait_time)
    

    
