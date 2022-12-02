from django.urls import path
from .views import *

urlpatterns = [
    # api
    path("api/feedback", FeedbackView.as_view(), name="feedback"),
    # page
    path("feedback/", FeedbackPage.as_view(), name="feedback"),
]
