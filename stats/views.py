from django.views import View
from users.models import StudentUser
from questions.models import Question
from rest_framework import generics
from .utils import dateLastStartOfWeek
from rest_framework.permissions import IsAuthenticated
from questions.serializers import QuestionSerializer
from django.http import HttpResponse, JsonResponse

import numpy as np
import pandas as pd

class SummaryList(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
       token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
       if " " not in token_header:
           return Question.objects.none()
       actual_token = token_header.split(" ")[1]
       user = StudentUser.objects.filter(auth_token=actual_token).first()
       if user == None or not user.is_ta:
           return Question.objects.none()

       # get all of the question
       last_date = dateLastStartOfWeek()
       questions = Question.objects.filter(ask_date__gte=last_date)
       return questions

class FrequentUserView(View):
    def get(self, request,  *args, **kwargs):

        token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
        if " " not in token_header:
            return JsonResponse({"authenticated": False})
        actual_token = token_header.split(" ")[1]
        user = StudentUser.objects.filter(auth_token=actual_token).first()
        if user == None or not user.is_superuser:
            return JsonResponse({"authenticated": False})

        all_questions = Question.objects.all()
        df = pd.DataFrame(list(all_questions.values()))
        results = df.groupby(by='author_email').author_email.count()
        response = results.to_dict()
        return JsonResponse(response)

class FrequentAnswerView(View):
    def get(self, request, *args, **kwargs):

        token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
        if " " not in token_header:
            return JsonResponse({"authenticated": False})
        actual_token = token_header.split(" ")[1]
        user = StudentUser.objects.filter(auth_token=actual_token).first()
        if user == None or not user.is_superuser:
            return JsonResponse({"authenticated": False})

        all_questions = Question.objects.all()
        df = pd.DataFrame(list(all_questions.values()))
        results = df.groupby(by='answered_by_email').answered_by_email.count()
        response = results.to_dict()
        return JsonResponse(response)