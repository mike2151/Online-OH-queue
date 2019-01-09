from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from .verify_tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import IntegrityError
import os

class UserSerializer(serializers.ModelSerializer):

    def validate_email(self, email):
        if "upenn.edu" not in email:
            raise serializers.ValidationError("Email is not a Penn Email")
            
        if "+" in email:
            raise serializers.ValidationError("No special characters allowed")
        
        user = None
        try:
            user = models.StudentUser.objects.get(email=email).first()
        except models.StudentUser.DoesNotExist:
            user = None
        if (user != None):
            if user.is_active:
                raise serializers.ValidationError("User already exists")

        return email

    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError('Password too short. Should be at least 8 characters.')
        return password

    class Meta:
        model = models.StudentUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('email', 'first_name', 'last_name', 'password', )

    def create(self, validated_data):
        
        user = models.StudentUser.objects.create(**validated_data)
        user.is_active = False
        user.username = user.email.split("@")[0]
        user.set_password(user.password)
        try:
            user.save()
        except IntegrityError:
            # need to delete the user that was created
            try:
                models.StudentUser.objects.get(email=user.email).delete()
            except:
                raise serializers.ValidationError("Email already in use")
            raise serializers.ValidationError("Email already in use")

        # email verification
        current_site = Site.objects.get(pk=1).domain
        course_title = os.environ.get('COURSE_TITLE', 'CIS 121')
        mail_subject = 'Activate your ' + course_title + ' Office Hours Account'
        message = "<p>Hi {name}, <br /> Please click on the link to confirm your registration for the {course_title} Office Hours Queue:  <br />{domain}/activate/{uid}/{token}  <br /> Best, <br /> {course_title} Staff</p>".format(course_title=course_title ,name=user.first_name, domain=current_site, uid=urlsafe_base64_encode(force_bytes(user.pk)).decode(), token=account_activation_token.make_token(user))
        to_email = user.email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()

        return user