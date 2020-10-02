from django.shortcuts import render
from .models import Task
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta

def home(request):
    # Making the main date changable, now only with left and right arrow
    date_change = 0
    if request.POST.get('next'):
        date_change = int(request.POST.get('next')) + 1
    elif request.POST.get('previous'):
        date_change = int(request.POST.get('previous')) - 1
    date_get = datetime.now() + timedelta(days = date_change)

    ''' TODO sync records with date and later with logged user '''
    db_data = Task.objects.filter(date__day = str(date_get.day),
                                  date__month = str(date_get.month),
                                  date__year = str(date_get.year) )

    data = {
        'date': date_get,
        'date_change': date_change,
        'db_data': db_data,
        'title': 'Tasks reminder'
    }
    return render(request, 'main/home.html', data)
