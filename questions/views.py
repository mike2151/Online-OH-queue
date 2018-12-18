from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from . import models
from . import serializers
from users.models import StudentUser

class QuestionCreationView(generics.ListCreateAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
        if token_header == None:
            return {'user': ''}
        # seperate token from Token xyz
        actual_token = token_header.split(" ")[1]
        user = StudentUser.objects.filter(auth_token=actual_token).first()
        return {'user': user.email}