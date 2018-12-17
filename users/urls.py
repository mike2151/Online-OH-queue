from django.urls import include, path

from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('login/', views.login),
]