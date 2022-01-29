from django.http import HttpResponse
from django.shortcuts import render
import models
# Create your views here.

def index(request):
    return HttpResponse("Hello, exchange market app")