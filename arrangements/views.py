from django.shortcuts import render,redirect
from .models import Activity, UserInfo
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def authenticate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(request, username=username, password=password)
    if not user:
        return redirect('login')
    auth.login(request, user)
    return redirect('index')


def signup(request):
    return render(request, 'signup.html')


def signup_submit(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        user = User.objects.create_user(username=username, password=password)
        info = UserInfo(user=user, nickname=username, gender=UserInfo.MALE, email=None)
        info.save()
        return redirect('login')
    except:
        return redirect('signup')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required
def set_info(request):
    return render(request, 'set_info.html')


@login_required
def set_info_submit(request):
    return redirect('index')


@login_required
def activities_list(request):
    return render(request, 'activities_list.html')


@login_required
def delete_activity(request, activity_id):
    return render(request, 'activities_list.html')


@login_required
@require_POST
def activity_info(request):
    return render(request, 'activity.html')


@login_required
def to_list(request):
    return redirect('activities-list')


@login_required
def search(request):
    return render(request, 'search.html')


@login_required
def search_submit(request):
    return render(request, 'search_result.html')


@login_required
def arrange(request):
    return render(request, 'arrangement.html')


@login_required
def type_in_single(request):
    return render(request, 'type_in_single.html')


@login_required
def type_in_single_submit(request):
    return redirect('type-in-single')


@login_required
def type_in_multi(request):
    return render(request, 'type_in_multi.html')


@login_required
def type_in_multi_submit(request):
    return redirect('type-in-multi')

