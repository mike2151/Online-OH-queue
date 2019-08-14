from django.shortcuts import render
from rest_framework import generics
from .models import Feedback
from .serializers import FeedbackSerializer
from django.http import HttpResponse, JsonResponse
from django.views import View
from users.models import StudentUser
from rest_framework.permissions import IsAuthenticated


class FeedbackCreationView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
        if token_header == None:
            return JsonResponse({"success": False, "error": "No authentication found"})
        actual_token = token_header.split(" ")[1]
        user = StudentUser.objects.filter(auth_token=actual_token).first()
        base_dict = {'user': user.email, 'was_helpful': self.request.POST.get("was_helpful", True)}
        if self.request.POST.get("helpful_scale", 0) != 0:
            base_dict["helpful_scale"] = self.request.POST.get("helpful_scale", 0)
        if len(self.request.POST.get("comments", "")) > 0:
            base_dict["comments"] = self.request.POST.get("comments", "")
        return base_dict

class NeedsToGiveFeedbackView(View):
    def get(self, request):
       token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
       if token_header == None or " " not in token_header:
           return JsonResponse({"needs_to_give_feedback": False})
       actual_token = token_header.split(" ")[1]
       user = StudentUser.objects.filter(auth_token=actual_token).first()
       if user == None:
           return JsonResponse({"needs_to_give_feedback": False})
       if user.is_ta:
           return JsonResponse({"needs_to_give_feedback": False})
       if user.num_questions_asked == 0:
           return JsonResponse({"needs_to_give_feedback": False})
       question = user.most_recent_question
       if question == None:
           return JsonResponse({"needs_to_give_feedback": False})
       if question.is_answered == False:
           return JsonResponse({"needs_to_give_feedback": False})
       if question.feedback_for_q != None:
           return JsonResponse({"needs_to_give_feedback": False})
       return JsonResponse({"needs_to_give_feedback": True})

class InfoForFeedback(View):
    def get(self, request):
       token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
       if token_header == None or " " not in token_header:
           return JsonResponse({"is_valid": False, "ta_name": "", "question": ""})
       actual_token = token_header.split(" ")[1]
       user = StudentUser.objects.filter(auth_token=actual_token).first()
       if user == None:
           return JsonResponse({"is_valid": False, "ta_name": "", "question": ""})
       if user.is_ta:
           return JsonResponse({"is_valid": False, "ta_name": "", "question": ""})
       if user.num_questions_asked == 0:
           return JsonResponse({"is_valid": False, "ta_name": "", "question": ""})
       question = user.most_recent_question
       if question == None:
           return JsonResponse({"is_valid": False, "ta_name": "", "question": ""})
       if question.is_answered == False:
           return JsonResponse({"is_valid": False, "ta_name": "", "question": ""})
       if question.feedback_for_q != None:
           return JsonResponse({"is_valid": False, "ta_name": "", "question": ""})
       
       ta_name = question.answerer_first_name + " " + question.answerer_last_name
       question = question.description
       return JsonResponse({"is_valid": True, "ta_name": ta_name, "question": question})