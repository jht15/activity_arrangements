from django.shortcuts import render, redirect, get_object_or_404
from .models import Activity, UserInfo
from .forms import UserInfoForm, ActivityForm, SearchForm, FileForm
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
        messages.warning(request, '登录失败！')
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
        messages.warning(request, '注册失败！')
        return redirect('signup')


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
        return redirect('set-info')


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
    messages.info(request, '删除成功！')
    return redirect('activities-list')



@login_required
def choose_activity_from_list(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.is_chosen = not activity.is_chosen
    activity.save()

    return redirect('activities-list')


@login_required
def activity_info(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    return render(request, 'activity.html', {'activity': activity})


@login_required
def to_list(request):
    return redirect('activities-list')


@login_required
def search_submit(request):
    form = SearchForm(request.POST) if request.method == 'POST' else None
    if form and form.is_valid() and form.has_changed():
        activities = []
        for item in auth.get_user(request).activities.all():
            item.is_search = True
            item.save()
            activities.append(item)
        if form.cleaned_data['name'] and form.cleaned_data['name'] != '':
            for item in activities:

                if item.name != form.cleaned_data['name']:

                    item.is_search = False
                    item.save()

        if form.cleaned_data['min_start_time'] and form.cleaned_data['min_start_time'] != '':
            for item in activities:
                if (item.start_time - form.cleaned_data['min_start_time']).seconds < 0:
                    item.is_search = False
                    item.save()
        if form.cleaned_data['max_start_time'] and form.cleaned_data['max_start_time'] != '':
            for item in activities:
                if (item.start_time - form.cleaned_data['max_start_time']).seconds > 0:
                    item.is_search = False
                    item.save()
        if form.cleaned_data['min_end_time'] and form.cleaned_data['min_end_time'] != '':
            for item in activities:
                if (item.end_time - form.cleaned_data['min_end_time']).seconds < 0:
                    item.is_search = False
                    item.save()
        if form.cleaned_data['max_end_time'] and form.cleaned_data['max_end_time'] != '':
            for item in activities:
                if (item.end_time - form.cleaned_data['max_end_time']).seconds > 0:
                    item.is_search = False
                    item.save()

        if form.cleaned_data['place'] and form.cleaned_data['place'] != '':
            for item in activities:
                if item.place != form.cleaned_data['place']:
                    item.is_search = False
                    item.save()
        if form.cleaned_data['type'] and form.cleaned_data['type'] != '':
            for item in activities:
                if item.type != form.cleaned_data['type']:
                    item.is_search = False
                    item.save()
        if form.cleaned_data['min_priority'] and form.cleaned_data['min_priority'] != '':
            for item in activities:
                if item.priority < form.cleaned_data['min_priority']:
                    item.is_search = False
                    item.save()
        if form.cleaned_data['min_enthusiasm'] and form.cleaned_data['min_enthusiasm'] != '':
            for item in activities:
                if item.enthusiasm < form.cleaned_data['min_enthusiasm']:
                    item.is_search = False
                    item.save()

        messages.info(request, '搜索完成！')
    else:
        messages.warning(request, '搜索失败！')
    return redirect('activities-list')



@login_required
def arrange(request):
    activities = []
    for activity in auth.get_user(request).activities.all():
        if activity.is_chosen:
            activities.append(activity)



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
        messages.info(request, '信息录入成功')
    else:
        messages.warning(request, '表单无效！')

    return redirect('type-in-single')


@login_required
def type_in_multi(request):
    return render(request, 'type_in_multi.html', {'form': FileForm()})


@login_required
def type_in_multi_submit(request):
    form = FileForm(request.POST) if request.method == 'POST' else None
    if form.is_valid():
        file = form.fields['file']
    
    return redirect('type-in-multi')

