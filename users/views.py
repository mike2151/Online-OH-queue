from rest_framework import generics

from . import models
from . import serializers

class UserListView(generics.ListCreateAPIView):
    queryset = models.StudentUser.objects.all()
    serializer_class = serializers.UserSerializer