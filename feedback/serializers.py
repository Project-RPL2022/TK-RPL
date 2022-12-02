from rest_framework import serializers

from main.utils import getHotelUser
from .models import *


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ['title', 'description']
