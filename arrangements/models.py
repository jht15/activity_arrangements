from django.db import models
from django.utils import timezone


class UserInfo(models.Model):
    user = models.OneToOneField('auth.user', related_name='user_info')
    nickname = models.CharField(max_length=20)
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)
    email = models.EmailField(blank=True, null=True)


class Activity(models.Model):
    user = models.ForeignKey('auth.user', related_name='activities', related_query_name='activity')
    name = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    priority = models.PositiveSmallIntegerField()
    place = models.CharField(max_length=50)
    enthusiasm = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=10)
    is_chosen = models.BooleanField(default=False)
    is_search = models.BooleanField(default=False)
    is_arranged = models.BooleanField(default=False)
    content = models.TextField()

# Create your models here.
