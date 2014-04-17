import hashlib
from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login, logout as dj_logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from models import UserProfile
from django.forms import EmailField
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from boto.s3.connection import S3Connection


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            temp_user = User.objects.get(username=username_md5(email))
            user = authenticate(username=temp_user.username, password=password)
            if user is not None and user.is_active:
                dj_login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Login successful!')
                return redirect('/accounts/dashboard')
            messages.add_message(request, messages.ERROR, 'Invalid login credentials!')
            return redirect('/accounts/login/')
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'User does not exist!')
            return redirect('/accounts/login/')
    else:
        return render(request, 'accounts/login.html')


@login_required
def logout(request):
    dj_logout(request)
    messages.add_message(request, messages.SUCCESS, 'You have successfully logged out!')
    return redirect('/')


@login_required
def s3storagehandler(request, access_key, secret_key):
    """
    Handles uploads and downloads to/from Amazon S3 service
    """
    if request.method == 'POST':
        conn = S3Connection(access_key, secret_key)


def email_signup(request):
    """
    Create a user profile w/ an email and password
    """
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if not unique_user(email):
            messages.add_message(request, messages.ERROR, 'That email is already registered!')
            return redirect('/accounts/signup')

        if not valid_email_address(email):
            messages.add_message(request, messages.ERROR, 'Invalid email address!')
            return redirect('/accounts/signup')

        valid_pw = check_valid_password(password, password_confirm)
        if not valid_pw:
            messages.add_message(request, messages.ERROR, 'Invalid password!')
            return redirect('/accounts/signup')

        user = User.objects.create_user(username_md5(email), email, password, first_name="", last_name="")
        user.save()
        userprofile = UserProfile(user=user)
        userprofile.save()
        auth_user = authenticate(username=username_md5(email), password=password)
        dj_login(request, auth_user)
        return redirect('/')
    else:
        return render(request, 'accounts/signup.html')


@login_required
def dashboard(request):
    """
    View for the dashboard
    """
    return render(request, 'website/dashboard.html')


def check_valid_password(pw, pw_conf):
    """
    Checks if the inputted passwords are greater then 8 characters and match
    """
    return len(pw) > 8 and pw == pw_conf


def unique_user(email):
    """
    Checks if the email is unique by comparing the hash of it
    """
    hashed_email = username_md5(email)
    if User.objects.filter(username=hashed_email).exists():
        return False
    else:
        return True


def username_md5(email):
    """
    Hashes the email using MD5 for the username
    """
    return hashlib.md5(email.lower()).hexdigest()[:30]


def valid_email_address(email):
    """
    Verify that the input is valid email format
    """
    try:
        EmailField().clean(email)
        return True
    except ValidationError:
        return False
