from django.shortcuts import render, redirect, get_object_or_404
from .models import Activity, UserInfo
from .forms import UserInfoForm, ActivityForm, SearchForm, FileForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import StreamingHttpResponse, HttpResponse
from django.utils import timezone
from .tasks import check


def index(request):
    if auth.get_user(request).is_authenticated:
        arranged_list = []
        for activity in auth.get_user(request).activities.all():
            if activity.is_arranged:
                arranged_list.append(activity)
        return render(request, 'index.html', {'user_info': auth.get_user(request).user_info, 'arranged_list': arranged_list})
    else:
        return render(request, 'index.html', {'user_info': None, 'arranged_list': None})


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
    return render(request, 'set_info.html', {'user_info': user_info, 'form_info': UserInfoForm({
        'nickname': user_info.nickname, 'gender': user_info.gender, 'email': user_info.email})})


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
                                                    'unchosen_unsearch_list': unchosen_unsearch_list
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
    form = ActivityForm({'name': activity.name, 'start_time': activity.start_time, 'end_time': activity.end_time,
                         'priority': activity.priority, 'place': activity.place, 'enthusiasm': activity.enthusiasm,
                         'type': activity.type, 'content': activity.content})
    return render(request, 'activity.html', {'activity': activity, 'form': form})


@login_required
def activity_info_submit(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    form = ActivityForm(request.POST) if request.method == 'POST' else None
    print(form)
    print(form.cleaned_data)
    if form.is_valid():
        activity.name = form.cleaned_data['name']
        activity.start_time = form.cleaned_data['start_time']
        activity.end_time = form.cleaned_data['end_time']
        activity.priority = form.cleaned_data['priority']
        activity.place = form.cleaned_data['place']
        activity.enthusiasm = form.cleaned_data['enthusiasm']
        activity.type = form.cleaned_data['type']
        activity.content = form.cleaned_data['content']
        activity.is_arranged = False
        activity.is_search = False
        activity.is_chosen = False
        activity.save()
        messages.info(request, '信息保存成功！')
    else:
        messages.warning(request, '信息更改失败！')
    return redirect('activity-info', activity.id)


@login_required
def to_list(request):
    return redirect('activities-list')


@login_required
def to_search(request):
    return render(request, 'search.html', {'search_form': SearchForm()})


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
                if item.start_time < form.cleaned_data['min_start_time']:
                    item.is_search = False
                    item.save()
        if form.cleaned_data['max_start_time'] and form.cleaned_data['max_start_time'] != '':
            for item in activities:
                if item.start_time > form.cleaned_data['max_start_time']:
                    item.is_search = False
                    item.save()
        if form.cleaned_data['min_end_time'] and form.cleaned_data['min_end_time'] != '':
            for item in activities:
                if item.end_time < form.cleaned_data['min_end_time']:
                    item.is_search = False
                    item.save()
        if form.cleaned_data['max_end_time'] and form.cleaned_data['max_end_time'] != '':
            for item in activities:
                if item.end_time > form.cleaned_data['max_end_time']:
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
        activity.is_arranged = False
        activity.save()
        if activity.is_chosen:
            activities.append(activity)

    arrange_list = []
    disarrange_list = []
    activities.sort(key=lambda a: (-a.priority, a.end_time))
    for activity in activities:
        flag = 1
        for aa in arrange_list:
            if aa.start_time < activity.end_time and aa.end_time > activity.start_time:
                flag = 0
                break
        if flag:
            arrange_list.append(activity)
            activity.is_arranged = True
            activity.save()

        else:
            disarrange_list.append(activity)
    arrange_list.sort(key=lambda a: (a.start_time, a.end_time))
    disarrange_list.sort(key=lambda a: (a.start_time, a.end_time))
    return render(request, 'arrangement.html', {'arrange_list': arrange_list, 'disarrange_list': disarrange_list})


def arranged_file(request):
    content = ''
    if auth.get_user(request).is_anonymous:
        return redirect('arrange')
    for activity in request.user.activities.all():
        if not activity.is_arranged:
            continue
        content += '活动名称: '
        content += activity.name
        content += '\n'
        content += '开始时间: '
        content += str(activity.start_time)
        content += '\n'
        content += '结束时间: '
        content += str(activity.end_time)
        content += '\n'
        content += '优先级: '
        content += str(activity.priority)
        content += '\n'
        content += '地点: '
        content += activity.place
        content += '\n'
        content += '热情度: '
        content += str(activity.enthusiasm)
        content += '\n'
        content += '类型: '
        content += activity.type
        content += '\n'
        content += '内容: '
        content += activity.content
        content += '\n'

    response = StreamingHttpResponse(content)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="MyArrangement.txt"'
    return response


@login_required
def type_in_single(request):
    form = ActivityForm()
    return render(request, 'type_in_single.html', {'form': form})


@login_required
def type_in_single_submit(request):
    form = ActivityForm(request.POST) if request.method == 'POST' else None
    if form.is_valid():
        if form.cleaned_data['start_time'] > form.cleaned_data['end_time']:
            messages.warning(request, '结束时间不能早于开始时间！')
            return redirect('type-in-single')

        activity = form.save(commit=False)
        activity.user = request.user
        activity.save()
        messages.info(request, '信息录入成功')
    else:
        messages.warning(request, '表单无效！')

    return redirect('type-in-single')


@login_required
def type_in_multi(request):
    return render(request, 'type_in_multi.html', {'form': FileForm()})


@login_required
def type_in_multi_submit(request):
    form = FileForm(request.POST, request.FILES) if request.method == 'POST' else None
    if form.is_valid():
        file = form.cleaned_data['file']
        name = file.name
        if name[-1] != 't' or name[-2] != 'x' or name[-3] != 't' or name[-4] != '.':
            messages.warning(request, '请上传.txt文件！')
            return redirect('type-in-multi')
        count = 0
        while True:
            form_name = file.readline()
            form_start_time = file.readline() if form_name else None
            form_end_time = file.readline() if form_start_time else None
            form_priority = file.readline() if form_end_time else None
            form_place = file.readline() if form_priority else None
            form_enthusiasm = file.readline() if form_place else None
            form_type = file.readline() if form_enthusiasm else None
            form_content = file.readline() if form_type else None
            if not form_content:
                break

            activity_form = ActivityForm({'name': form_name, 'start_time': form_start_time,
                                          'end_time': form_end_time, 'priority': int(form_priority),
                                          'place': form_place, 'enthusiasm': int(form_enthusiasm),
                                          'type': form_type, 'content': form_content})
            if activity_form.is_valid():
                if activity_form.cleaned_data['start_time'] > activity_form.cleaned_data['end_time']:
                    continue
                count += 1
                activity = activity_form.save(commit=False)
                activity.user = request.user
                activity.save()
            else:
                break
        messages.info(request, '录入了' + str(count) + '个有效的活动信息')
    return redirect('type-in-multi')

