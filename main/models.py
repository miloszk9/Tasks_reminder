from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Task(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    create_date = models.DateTimeField(auto_now_add = True)
    date = models.DateTimeField(default = timezone.now)
    state = False
    
    def __str__(self):
        return self.name
    
    # Changing the state of the task, e.g. True == done, False == not done yet
    def state_change(self):
        if state == True:
            state = False
        else:
            state = True
