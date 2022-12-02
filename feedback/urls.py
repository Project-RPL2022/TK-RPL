from django.urls import path
from .views import *

urlpatterns = [
    path("", FeedbackView.as_view(), name="feedback"),
]
