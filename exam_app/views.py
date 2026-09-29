from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from . import models

def index(request):
    return render(request, 'index.html')