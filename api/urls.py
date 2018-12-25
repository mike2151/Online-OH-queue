from django.urls import include, re_path, path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('users/', include('users.urls')),
    path('queue/', include('ohqueue.urls')),
    path('questions/', include('questions.urls')),
]