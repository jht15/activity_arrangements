from django.shortcuts import render, redirect, get_object_or_404
from .models import Activity, UserInfo
from .forms import UserInfoForm, ActivityForm, SearchForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from datetime import datetime


def index(request):
    if auth.get_user(request).is_authenticated:
        return render(request, 'index.html', {'user_info': auth.get_user(request).user_info})
    else:
        return render(request, 'index.html', {'user_info': None})


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
        return redirect('index')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required
def set_info(request):
    user_info = auth.get_user(request).user_info
    return render(request, 'set_info.html', {'user_info': user_info, 'form_info': UserInfoForm()})


@login_required
def set_info_submit(request):
    form = UserInfoForm(request.POST) if request.method == 'POST' else None
    user_info = auth.get_user(request).user_info

    if form.is_valid():

        temp = form.save(commit=False)
        user_info.nickname = temp.nickname
        user_info.gender = temp.gender
        user_info.email = temp.email
        user_info.save()
        return redirect('index')

    else:
        messages.warning(request, '输入了无效的用户信息')
        return render(request, 'set_info.html', {'user_info': user_info, 'form_info': UserInfoForm()})


@login_required
def activities_list(request):
    chosen_search_list = []
    chosen_unsearch_list = []
    unchosen_search_list = []
    unchosen_unsearch_list = []

    for item in auth.get_user(request).activities.all():
        if item.is_chosen:
            if item.is_search:
                chosen_search_list.append(item)
            else:
                chosen_unsearch_list.append(item)
        else:
            if item.is_search:
                unchosen_search_list.append(item)
            else:
                unchosen_unsearch_list.append(item)
    return render(request, 'activities_list.html', {'chosen_search_list': chosen_search_list,
                                                    'chosen_unsearch_list': chosen_unsearch_list,
                                                    'unchosen_search_list': unchosen_search_list,
                                                    'unchosen_unsearch_list': unchosen_unsearch_list,
                                                    'search_form': SearchForm()
                                                    })


@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.delete()
    chosen_search_list = []
    chosen_unsearch_list = []
    unchosen_search_list = []
    unchosen_unsearch_list = []

    for item in auth.get_user(request).activities.all():
        if item.is_chosen:
            if item.is_search:
                chosen_search_list.append(item)
            else:
                chosen_unsearch_list.append(item)
        else:
            if item.is_search:
                unchosen_search_list.append(item)
            else:
                unchosen_unsearch_list.append(item)

    return render(request, 'activities_list.html', {'chosen_search_list': chosen_search_list,
                                                    'chosen_unsearch_list': chosen_unsearch_list,
                                                    'unchosen_search_list': unchosen_search_list,
                                                    'unchosen_unsearch_list': unchosen_unsearch_list,
                                                    'search_form': SearchForm()
                                                    })



@login_required
def choose_activity_from_list(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.is_chosen = not activity.is_chosen
    activity.save()
    chosen_search_list = []
    chosen_unsearch_list = []
    unchosen_search_list = []
    unchosen_unsearch_list = []

    for item in auth.get_user(request).activities.all():
        if item.is_chosen:
            if item.is_search:
                chosen_search_list.append(item)
            else:
                chosen_unsearch_list.append(item)
        else:
            if item.is_search:
                unchosen_search_list.append(item)
            else:
                unchosen_unsearch_list.append(item)

    return render(request, 'activities_list.html', {'chosen_search_list': chosen_search_list,
                                                    'chosen_unsearch_list': chosen_unsearch_list,
                                                    'unchosen_search_list': unchosen_search_list,
                                                    'unchosen_unsearch_list': unchosen_unsearch_list,
                                                    'search_form': SearchForm()
                                                    })


@login_required
def activity_info(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    return render(request, 'activity.html', {'activity': activity})


@login_required
def to_list(request):
    chosen_search_list = []
    chosen_unsearch_list = []
    unchosen_search_list = []
    unchosen_unsearch_list = []

    for item in auth.get_user(request).activities.all():
        if item.is_chosen:
            if item.is_search:
                chosen_search_list.append(item)
            else:
                chosen_unsearch_list.append(item)
        else:
            if item.is_search:
                unchosen_search_list.append(item)
            else:
                unchosen_unsearch_list.append(item)

    return render(request, 'activities_list.html', {'chosen_search_list': chosen_search_list,
                                                    'chosen_unsearch_list': chosen_unsearch_list,
                                                    'unchosen_search_list': unchosen_search_list,
                                                    'unchosen_unsearch_list': unchosen_unsearch_list,
                                                    'search_form': SearchForm()
                                                    })


@login_required
def search_submit(request):
    form = SearchForm(request.POST) if request.method == 'POST' else None
    if form and form.is_valid():

        activities = []
        for item in auth.get_user(request).activities.all():
            activities.append(item)

        if form.name and form.name != '':
            for item in activities:
                if item.name != form.name:
                    item.is_search = False
                    item.save()
                    activities.remove(item)
        if form.min_start_time and form.min_start_time != '':
            for item in activities:
                if (item.start_time - form.min_start_time).seconds < 0:
                    item.is_search = False
                    item.save()
                    activities.remove(item)
        if form.max_start_time and form.max_start_time != '':
            for item in activities:
                if (item.start_time - form.max_start_time).seconds > 0:
                    item.is_search = False
                    item.save()
                    activities.remove(item)
        if form.min_end_time and form.min_end_time != '':
            for item in activities:
                if (item.end_time - form.min_end_time).seconds < 0:
                    item.is_search = False
                    item.save()
                    activities.remove(item)
        if form.max_end_time and form.max_end_time != '':
            for item in activities:
                if (item.end_time - form.max_end_time).seconds > 0:
                    item.is_search = False
                    item.save()
                    activities.remove(item)

        if form.place and form.place != '':
            for item in activities:
                if item.place != form.place:
                    item.is_search = False
                    item.save()
                    activities.remove(item)
        if form.type and form.type != '':
            for item in activities:
                if item.type != form.type:
                    item.is_search = False
                    item.save()
                    activities.remove(item)
        if form.min_priority and form.min_priority != '':
            for item in activities:
                if item.priority < form.min_priority:
                    item.is_search = False
                    item.save()
                    activities.remove(item)
        if form.min_enthusiasm and form.min_enthusiasm != '':
            for item in activities:
                if item.enthusiasm < form.min_enthusiasm:
                    item.is_search = False
                    item.save()
                    activities.remove(item)
        for item in activities:
            item.is_search = True
            item.save

    chosen_search_list = []
    chosen_unsearch_list = []
    unchosen_search_list = []
    unchosen_unsearch_list = []

    for item in auth.get_user(request).activities.all():
        if item.is_chosen:
            if item.is_search:
                chosen_search_list.append(item)
            else:
                chosen_unsearch_list.append(item)
        else:
            if item.is_search:
                unchosen_search_list.append(item)
            else:
                unchosen_unsearch_list.append(item)

    return render(request, 'activities_list.html', {'chosen_search_list': chosen_search_list,
                                                    'chosen_unsearch_list': chosen_unsearch_list,
                                                    'unchosen_search_list': unchosen_search_list,
                                                    'unchosen_unsearch_list': unchosen_unsearch_list,
                                                    'search_form': SearchForm()
                                                    })



@login_required
def arrange(request):
    activities = []
    for activity in auth.get_user(request).activities.all():
        if activity.is_chosen:
            activities.add(activity)



    arrange_list = []
    disarrange_list = []
    return render(request, 'arrangement.html', {'arrange_list': arrange_list, 'disarrange_list': disarrange_list})


@login_required
def type_in_single(request):
    form = ActivityForm()
    return render(request, 'type_in_single.html', {'form': form})


@login_required
def type_in_single_submit(request):
    form = ActivityForm(request.POST) if request.method == 'POST' else None
    if form.is_valid():
        activity = form.save(commit=False)
        activity.user = request.user
        activity.save()
        form = ActivityForm()
    return render(request, 'type_in_single.html', {'form': form})


@login_required
def type_in_multi(request):
    return render(request, 'type_in_multi.html')


@login_required
def type_in_multi_submit(request):
    return redirect('type-in-multi')

