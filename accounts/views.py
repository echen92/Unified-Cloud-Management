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
from courses.models import Course
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

import courses.recommender as recommender


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
                return redirect('/accounts/profile/')
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
    return redirect('/')


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
        return redirect('/subject_preferences')
    else:
        return render(request, 'accounts/signup.html')


@receiver(user_signed_up)
def create_user_profile_for_socialaccount(sender, **kwargs):
    user = kwargs['user']
    user.username = username_md5(user.email)
    userprofile = UserProfile(user=user)
    userprofile.save()


@login_required
def profile(request):
    """
    View for the user profile page
    """
    current_user = request.user
    user_profile = UserProfile.objects.get(user=current_user)
    enrolled_list = list(user_profile.enrolled.all())
    recommend_list = get_recommended_courses(user_profile)
    return render(request, 'accounts/profile.html', {"email": current_user.email, "enrolled_list": enrolled_list,
                                                     "recommend_list": recommend_list})


def get_recommended_courses(user_profile):
    current_user = user_profile.user
    user_based_rec = recommender.get_all_user_recommendations(current_user)
    subject_based_rec = recommender.get_all_subject_recommendations(current_user)
    
    # start with an empty list
    recommendations = []

    # add user based recommendations first
    for course in user_based_rec:
        recommendations.append(course)

    # add subject based recommendation next
    for course in subject_based_rec:
        recommendations.append(course)

    num_random_needed = 5 - len(recommendations)
    if num_random_needed > 0:
        random_courses = get_random_courses(num_random_needed)
        for course in random_courses:
            recommendations.append(course)

    return recommendations[:5]

def get_random_courses(num):
    """
    Gets a bunch of random courses
    """
    random_courses = list()
    random_course_order = Course.objects.order_by('?')
    for i in range(num):
        random_courses.append(random_course_order[i])
    return random_courses


@login_required
def deactivate_account(request):
    """
    Deletes the user account from the database
    """
    current_user = request.user
    current_user.is_active = False  # Django convention to avoid breaking foreign keys if they exist
    current_user.save()
    dj_logout(request)
    return redirect('/')


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

@login_required
def change_password(request):
    """
    Changes the user's password
    """
    if request.method == 'POST':
        current_user = request.user
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if not check_valid_password(password, password_confirm):
            messages.add_message(request, messages.ERROR, 'Invalid password!')
        else:
            current_user.set_password(password)
            current_user.save()
            messages.add_message(request, messages.SUCCESS, 'Password updated!')
    
    return redirect('/accounts/profile/')


@login_required
def change_email(request):
    """
    Changes the user's email
    """
    if request.method == 'POST':
        current_user = request.user
        new_email = request.POST.get('new_email')

        if not valid_email_address(new_email):
            messages.add_message(request, messages.ERROR, 'Invalid email!')
        elif not unique_user(new_email):
            print(User.objects.filter(username=username_md5(new_email)))
            messages.add_message(request, messages.ERROR, 'Email already exists!')
        else:
            current_user.email = new_email
            current_user.username = username_md5(new_email)
            current_user.save()
            messages.add_message(request, messages.SUCCESS, 'Email updated!')

    return redirect('/accounts/profile/')


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
