from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('needs_to_give_feedback/', views.NeedsToGiveFeedbackView.as_view(), name="needs_to_give_feedback"),
    path('info_for_feedback/', views.InfoForFeedback.as_view(), name="info_for_feedback"),
    path('post_feedback/', views.FeedbackCreationView.as_view(), name='feedback'),
]