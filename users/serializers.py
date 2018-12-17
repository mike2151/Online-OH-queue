from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):

    def validate_email(self, email):
        if "upenn.edu" not in email:
            raise serializers.ValidationError("Email is not a Penn Email")
        return email

    class Meta:
        model = models.StudentUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user =  models.StudentUser.objects.create(**validated_data)
        user.is_active = False
        user.save()
        return user