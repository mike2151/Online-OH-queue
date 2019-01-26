from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('is_ta/', views.taAuthenticationView.as_view(), name="is_ta"),
]