from django.views import View
from .models import Question
from django.http import JsonResponse
from users.models import StudentUser
from ohqueue.models import OHQueue
import json

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
       # remove from the queue
       queue.questions.remove(question)
       queue.save()

       return JsonResponse({"success": True})