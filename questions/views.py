from django.views import View
from .models import Question
from django.http import JsonResponse
from users.models import StudentUser
from ohqueue.models import OHQueue
import json
import datetime

class QuestionAnswerView(View):
    def post(self, request,  *args, **kwargs):
       # get current TA
       token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
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
            return JsonResponse({"error": "Question does not exist"})
       
       # mark question as resolved and TA answered
       question.is_answered = True
       question.answered_by_email = user.email
       question.save()

       # edit average wait time
       
       time_diff_question_answered_ask = datetime.datetime.now() - quesiton.ask_date
       time_since_last_answer = datetime.datetime.now() - queue.last_answer_time

       new_num_answered = queue.num_questions_answered + 1
       old_average = queue.average_wait_time

       # see if one hour ago so we reset
       if (time_since_last_answer.hours >= 1):
          new_num_answered = 1
          old_average = 0
     

       old_sum = old_average * (new_num_answered - 1)
       new_sum = old_sum + time_diff_question_answered_ask.minutes
       new_average = round((float(new_sum) / float(new_num_answered), 1))
       
       queue.average_wait_time = new_average
       queue.num_questions_answered = new_num_answered
       queue.last_answer_time = datetime.datetime.now()

       # remove from the queue
       queue.questions.remove(question)
       queue.save()

       return JsonResponse({"success": True})