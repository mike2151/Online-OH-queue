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

class UserRegisterView(generics.CreateAPIView):
    queryset = models.StudentUser.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        # see if inactive account. If so, resend email
        attempt_email = request.data.get("email")
        user = None
        try:
            user = (models.StudentUser.objects.get(email=attempt_email))
        except models.StudentUser.DoesNotExist:
            user = None
        if user != None:
            if not user.is_active:
                # resend confirmation email
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
                return HttpResponse(status=201)
            else:
                return super(UserRegisterView, self).create(request, *args, **kwargs)
        else:
            return super(UserRegisterView, self).create(request, *args, **kwargs)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = models.StudentUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('/activated')
    else:
        return HttpResponse('Activation link is invalid!')


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
@throttle_classes([AnonRateThrottle,])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

class taAuthenticationView(View):
    # return the email because some views also need the email of the TA
    def get(self, request):
       token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
       if token_header == None or " " not in token_header:
           return JsonResponse({"is_ta": False, "email": ""})
       actual_token = token_header.split(" ")[1]
       user = models.StudentUser.objects.filter(auth_token=actual_token).first()
       if user == None:
           return JsonResponse({"is_ta": False, "email": ""})
       if not user.is_ta:
           return JsonResponse({"is_ta": False, "email": user.email})
       return JsonResponse({"is_ta": True})

