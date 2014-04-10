from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from courses.models import Subject, Course
# from accounts.models import UserProfile
from django.http import HttpResponse
import json


def index(request):
    return render(request, 'website/index.html')