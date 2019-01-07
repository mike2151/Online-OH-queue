from django.views import View
from .models import Question
from django.http import JsonResponse
from users.models import StudentUser
from ohqueue.models import OHQueue
import json
import datetime
from django.conf import settings
import pytz
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.views.decorators.csrf import csrf_exempt
import os

class QuestionInformation(View):
     def get(self, request, *args, **kwargs):
       token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
       actual_token = token_header.split(" ")[1]
       user = StudentUser.objects.filter(auth_token=actual_token).first()
       if user == None:
           return JsonResponse({"success": False, "error": "You are not authenticated"})
       question_id = (self.kwargs["questionid"])
       question = Question.objects.filter(id=question_id).first()
       if question == None:
            return JsonResponse({"success": False, "error": "Not a valid question"})
       if question.author_email != user.email:
            return JsonResponse({"success": False, "error": "Not the author of the question"})
       return JsonResponse({"success": True, "description": question.description})

class QuestionDeleteView(View):
     @csrf_exempt
     def post(self, request,  *args, **kwargs):
       token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
       if token_header == None or " " not in token_header:
           return JsonResponse({"success": False, "error": "You are not authenticated"})
       actual_token = token_header.split(" ")[1]
       user = StudentUser.objects.filter(auth_token=actual_token).first()
       if user == None:
           return JsonResponse({"success": False, "error": "You are not authenticated"}) 
       question_id = (json.loads(request.body.decode())["question_id"])
       question = None
       try:
          question = Question.objects.get(id=question_id)
       except Question.DoesNotExist:
          question = None
       if question == None:
            return JsonResponse({"success": False, "error": "Question does not exist"})
       if question.author_email != user.email:
            return JsonResponse({"success": False, "error": "You are not authenticated"}) 
       question.delete()
       layer = get_channel_layer()
       async_to_sync(layer.group_send)(
            'ohqueue',
            {
                'type': 'ohqueue.update',
                'message': 'update'
            }
        )
       return JsonResponse({"success": True})

class QuestionAnswerView(View):
   
    def convert_timedelta_to_hours(self, duration):
     days, seconds = duration.days, duration.seconds
     hours = days * 24 + seconds // 3600
     minutes = (seconds % 3600) // 60
     seconds = (seconds % 60)
     return hours

    def convert_timedelta_to_minutes(self, duration):
     days, seconds = duration.days, duration.seconds
     minutes = (seconds % 3600) // 60
     seconds = (seconds % 60)
     return minutes 

    @csrf_exempt
    def post(self, request,  *args, **kwargs):
       # get current TA
       token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
       if token_header == None or " " not in token_header:
           return JsonResponse({"success": False, "error": "You are not authenticated"})
       actual_token = token_header.split(" ")[1]
       user = StudentUser.objects.filter(auth_token=actual_token).first()
       if user == None or not user.is_ta:
           return JsonResponse({"success": False, "error": "You are not authenticated"})

       # get queue
       queue_name = (json.loads(request.body.decode())["queue"])
       queue = None
       try:
            queue = OHQueue.objects.get(name=queue_name)
       except:
            queue = None
       if queue == None:
            return JsonResponse({"success": False, "error": "Queue does not exist"})
       # get question
       question_id = (json.loads(request.body.decode())["question_id"])
       question = None
       try:
            question = Question.objects.get(pk=question_id)
       except:
            question = None
       if question == None:
            return JsonResponse({"success": False, "error": "Question does not exist"})
       
       # mark question as resolved and TA answered
       question.is_answered = True
       question.answered_by_email = user.email
       question.answerer_first_name = user.first_name
       question.answerer_last_name = user.last_name
       question.host_queue = queue_name
       question.save()

       # edit average wait time
       curr_time_zone = pytz.timezone(os.environ.get('QUEUE_TIME_ZONE','America/New_York'))

       question_answer_time_local = datetime.datetime.now(curr_time_zone) 

       wait_time_between_question = question_answer_time_local - queue.last_answer_time

       new_num_answered = queue.num_questions_answered + 1

       old_average = queue.average_wait_time

       # see if one hour ago so we reset
       hours_dif = self.convert_timedelta_to_hours(wait_time_between_question)
       if (hours_dif >= 1 or hours_dif < 0):
          new_num_answered = 1
          old_average = 0
          wait_time_between_question = datetime.timedelta(seconds=0)

       old_sum = old_average * (new_num_answered - 1)
       new_sum = old_sum + self.convert_timedelta_to_minutes(wait_time_between_question)
       new_average = round((float(new_sum) / float(new_num_answered)), 1)
       
       queue.average_wait_time = new_average
       queue.num_questions_answered = new_num_answered
       # answer time is set in current time zone
       queue.last_answer_time = question_answer_time_local

       # remove from the queue
       queue.questions.remove(question)
       queue.save()

       layer = get_channel_layer()
       async_to_sync(layer.group_send)(
            'ohqueue',
            {
                'type': 'ohqueue.update',
                'message': 'update'
            }
        )

       return JsonResponse({"success": True})