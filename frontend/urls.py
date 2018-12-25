from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
import users.views as userviews

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('signup/', TemplateView.as_view(template_name='index.html')),
    path('login/', TemplateView.as_view(template_name='index.html')),
    path('answer/', TemplateView.as_view(template_name='index.html')),
    path('<queuename>/ask', TemplateView.as_view(template_name='index.html')),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        userviews.activate, name='activate'),
]