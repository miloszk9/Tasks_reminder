from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class Birthdate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField()

class Task(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    date_create = models.DateTimeField(auto_now_add = True, blank=True)
    todo_timestamp = models.DateTimeField()
    todo_date = models.DateField()
    is_done = models.BooleanField(default = False)

    def __str__(self):
        return self.name
    
class Friends(models.Model):
    user1 = models.ForeignKey(User, related_name='user1', on_delete = models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2', on_delete = models.CASCADE)
    is_accepted = models.BooleanField(default = False)

class Holidays(models.Model):
    name = models.CharField(max_length = 100)
    date = models.DateField()
