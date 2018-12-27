from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import OHQueue
from questions.models import Question
from .serializers import OHQueueSerializer
from questions.serializers import QuestionSerializer
from rest_framework.response import Response
from users.models import StudentUser
from django.http import JsonResponse


class OHQueueCreationView(generics.CreateAPIView):
    queryset = OHQueue.objects.all()
    serializer_class = OHQueueSerializer
    permission_classes = (IsAdminUser,)

class OHQueueListView(generics.ListAPIView):
    queryset = OHQueue.objects.all()
    serializer_class = OHQueueSerializer
    permission_classes = (IsAuthenticated,)

class QuestionCreationView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        ohqueuename = (self.kwargs["name"])
        token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
        if token_header == None:
            return JsonResponse({"error": "No authentication found"})
        # seperate token from Token xyz
        actual_token = token_header.split(" ")[1]
        user = StudentUser.objects.filter(auth_token=actual_token).first()
        return {'user': user.email, 'user-first-name': user.first_name, 'user-last-name': user.last_name, 'queue': ohqueuename}