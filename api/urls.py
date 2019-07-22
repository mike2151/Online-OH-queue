from django.urls import include, re_path, path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from stats.views import SummaryList
from .views import GetThemeVariablesView


urlpatterns = [
    path('users/', include('users.urls')),
    path('feedback/', include('feedback.urls')),
    path('queue/', include('ohqueue.urls')),
    path('questions/', include('questions.urls')),
    path('summary/', SummaryList.as_view(), name="summary"),
    path('stats/', include('stats.urls')),
    path('theme/', GetThemeVariablesView.as_view() ,name="theme"),
]
