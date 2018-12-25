from django.views import View
from .models import Question
from django.http import JsonResponse
from users.models import StudentUser

def QuestionAnswerView(View):
    def post(self, request):
       # get current TA
       token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
       actual_token = token_header.split(" ")[1]
       user = StudentUser.objects.filter(auth_token=actual_token).first()
       if not user.is_ta:
           return JsonResponse({"error": "You are not authenticated"})

       # get question
       question_id = request.POST["pk"]
       question = None
       try:
            question = question_id.objects.get(pk=question_id)
       except:
            question = None
       if question == None:
            return JsonResponse({"error": "Question does not exist"})
       
       # mark question as resolved and TA answered
       question.is_answered = True
       question.answered_by_email = user.email
       question.save()
       return JsonResponse({"success": "true"})