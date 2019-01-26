from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from django.utils.encoding import force_bytes, force_text
from .verify_tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

from rest_framework import generics
from rest_framework.throttling import AnonRateThrottle
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
import os

from . import models
from . import serializers

class taAuthenticationView(View):
    # return the email because some views also need the email of the TA
    def get(self, request):
       if request.user == None:
           return JsonResponse({"is_ta": False, "email": ""})
       if not request.user.is_ta:
           return JsonResponse({"is_ta": False, "email": request.user.email})
       return JsonResponse({"is_ta": True})

