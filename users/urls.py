from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('is_ta/', views.taAuthenticationView.as_view(), name="is_ta"),
    path('update/', views.UpdateUserView.as_view(), name="userinfo"),
    path('needs_update/', views.NeedsUpdateView.as_view(), name="needs_update"),
]