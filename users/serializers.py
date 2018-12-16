from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentUser
        fields = ('email', 'first_name', 'last_name')