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


class SearchForm(forms.Form):
    name = forms.CharField(max_length=50, required=False)
    min_start_time = forms.DateTimeField(required=False)
    max_start_time = forms.DateTimeField(required=False)
    min_end_time = forms.DateTimeField(required=False)
    max_end_time = forms.DateTimeField(required=False)

    place = forms.CharField(max_length=50, required=False)
    type = forms.CharField(max_length=10, required=False)
    min_priority = forms.IntegerField(required=False)
    min_enthusiasm = forms.IntegerField(required=False)


class FileForm(forms.Form):
    file = forms.FileField()
