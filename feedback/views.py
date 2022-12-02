from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from main.utils import getHotelUser

from .serializers import *
from .models import *


class FeedbackView(APIView):
    def post(self, request, format=None):
        username = request.user

        serializer = FeedbackSerializer(
            data=request.data
        )
        if serializer.is_valid():
            Feedback.objects.create(
                title=request.data['title'],
                description=request.data['description'],
                sender=getHotelUser(username)
            )

        return Response({'msg': 'success'})

# pages


class FeedbackPage(APIView):
    def get(self, request, format=None):
        return render(request, 'feedback/index.html')
