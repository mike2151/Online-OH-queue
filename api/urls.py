from django.urls import include, re_path, path
from django.views.generic import TemplateView
from rest_auth.registration.views import VerifyEmailView
from django.views.generic.base import RedirectView


urlpatterns = [
    path('users/', include('users.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    re_path(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', RedirectView.as_view(url='/', permanent=False),
            name='account_confirm_email'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', RedirectView.as_view(url='/', permanent=False),
            name='account_confirm_email'),
]