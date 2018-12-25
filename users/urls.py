from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('login/', views.login),
    path('is_ta/', views.taAuthenticationView.as_view(), name="is_ta")
]