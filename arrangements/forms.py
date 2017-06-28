from django import forms
from .models import Activity, UserInfo


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('nickname', 'gender', 'email')


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('name', 'start_time', 'end_time', 'priority', 'place', 'enthusiasm', 'type', 'content')
