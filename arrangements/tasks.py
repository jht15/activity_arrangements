from __future__ import absolute_import
from activity_arrangements.celery import app
from .models import Activity
from django.core.mail import send_mail
from datetime import datetime
from django.utils import timezone


@app.task(name='tasks.check')
def check():
    print('hello')
    activities = Activity.objects.all()
    time = timezone.now()
    print(time)
    for activity in activities:
        print('name' + activity.name)
        print('start')
        print(activity.start_time)
        print((activity.start_time - time).days)
        print((activity.start_time - time).seconds)
        print(activity.is_arranged)
        if activity.is_arranged and not (activity.start_time - time).days and (activity.start_time - time).seconds > \
                82800 and activity.user.user_info.email:
            send_status = send_mail('活动提醒', '尊敬的' + activity.user.user_info.nickname + '您的活动' + activity.name + '将在一天内开始！', 'thss_arrange@sina.com',
                                    [activity.user.user_info.email])
            print('发送：')
            print(send_status)
            print(activity.user.user_info.email)
    return True
