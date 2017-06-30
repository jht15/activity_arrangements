from django.shortcuts import render, redirect, get_object_or_404
from .models import Activity, UserInfo
from .forms import UserInfoForm, ActivityForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages


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
                chosen_search_list.add(item)
            else:
                chosen_unsearch_list.add(item)
        else:
            if item.is_search:
                unchosen_search_list.add(item)
            else:
                unchosen_unsearch_list.add(item)

    return render(request, 'activities_list.html', {'chosen_search_list': chosen_search_list,
                                                    'chosen_unsearch_list': chosen_unsearch_list,
                                                    'unchosen_search_list': unchosen_search_list,
                                                    'unchosen_unsearch_list': unchosen_unsearch_list
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
                chosen_search_list.add(item)
            else:
                chosen_unsearch_list.add(item)
        else:
            if item.is_search:
                unchosen_search_list.add(item)
            else:
                unchosen_unsearch_list.add(item)

    return render(request, 'activities_list.html', {'chosen_search_list': chosen_search_list,
                                                    'chosen_unsearch_list': chosen_unsearch_list,
                                                    'unchosen_search_list': unchosen_search_list,
                                                    'unchosen_unsearch_list': unchosen_unsearch_list
                                                    })



@login_required
def choose_activity_from_list(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.is_chosen = not activity.is_chosen
    chosen_search_list = []
    chosen_unsearch_list = []
    unchosen_search_list = []
    unchosen_unsearch_list = []

    for item in auth.get_user(request).activities.all():
        if item.is_chosen:
            if item.is_search:
                chosen_search_list.add(item)
            else:
                chosen_unsearch_list.add(item)
        else:
            if item.is_search:
                unchosen_search_list.add(item)
            else:
                unchosen_unsearch_list.add(item)

    return render(request, 'activities_list.html', {'chosen_search_list': chosen_search_list,
                                                    'chosen_unsearch_list': chosen_unsearch_list,
                                                    'unchosen_search_list': unchosen_search_list,
                                                    'unchosen_unsearch_list': unchosen_unsearch_list
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
                chosen_search_list.add(item)
            else:
                chosen_unsearch_list.add(item)
        else:
            if item.is_search:
                unchosen_search_list.add(item)
            else:
                unchosen_unsearch_list.add(item)

    return render(request, 'activities_list.html', {'chosen_search_list': chosen_search_list,
                                                    'chosen_unsearch_list': chosen_unsearch_list,
                                                    'unchosen_search_list': unchosen_search_list,
                                                    'unchosen_unsearch_list': unchosen_unsearch_list
                                                    })


@login_required
def search_submit(request):
    activities = auth.get_user(request).activities.all()
    search_list = []

    #for activity in activities:
        #if
            #search_list.append(activity)
            #activity.is_search = True

    chosen_search_list = []
    chosen_unsearch_list = []
    unchosen_search_list = []
    unchosen_unsearch_list = []

    for item in auth.get_user(request).activities.all():
        if item.is_chosen:
            if item.is_search:
                chosen_search_list.add(item)
            else:
                chosen_unsearch_list.add(item)
        else:
            if item.is_search:
                unchosen_search_list.add(item)
            else:
                unchosen_unsearch_list.add(item)

    return render(request, 'activities_list.html', {'chosen_search_list': chosen_search_list,
                                                    'chosen_unsearch_list': chosen_unsearch_list,
                                                    'unchosen_search_list': unchosen_search_list,
                                                    'unchosen_unsearch_list': unchosen_unsearch_list
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
        activity = form.save()
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

