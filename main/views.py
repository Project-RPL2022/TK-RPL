from django.shortcuts import render
from django.http import HttpResponse
from tkrpl.auth import *

# Create your views here.
def index(request):
    user = request.user
    return render(request, 'home.html', {'user' : user})