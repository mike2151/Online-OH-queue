from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
import users.views as userviews
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('answer/', TemplateView.as_view(template_name='index.html')),
    path('feedback/', TemplateView.as_view(template_name='index.html')),
    path('userinfo/', TemplateView.as_view(template_name='index.html')),
    path('summary/', TemplateView.as_view(template_name='index.html')),
    path('statistics/', TemplateView.as_view(template_name='index.html')),
    path('<queuename>/ask/', TemplateView.as_view(template_name='index.html')),
    path('<questionid>/edit/', TemplateView.as_view(template_name='index.html')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
