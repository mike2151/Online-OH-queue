from django.urls import include, path

from . import views

urlpatterns = [
    path('/frequent', views.FrequentUserView.as_view())
]