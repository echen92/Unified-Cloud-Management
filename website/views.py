from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def index(request):
    if request.user.is_authenticated():
        return redirect('/dashboard')
    else:
        return render(request, 'website/index.html')

@login_required
def dashboard(request):
    return render(request, 'website/dashboard.html')

