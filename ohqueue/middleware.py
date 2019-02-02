from users.models import StudentUser
from django.contrib import auth
from django.urls import reverse
from django.shortcuts import redirect
from django.urls import resolve

class ShibbolethMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.META.get("HTTP_EPPN"):
            username = request.META["HTTP_EPPN"]
            user, _ = StudentUser.objects.get_or_create(username=username, defaults={"email":username, "first_name": "None", "last_name": "None"})
            request.user = user
            auth.login(request, user)
            setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response