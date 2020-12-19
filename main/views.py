from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Task
from django.utils import timezone
from datetime import datetime
from datetime import timedelta

def login_page(request):
    # If user is logged in
    if request.user.id != None:
        return redirect('home')

    if request.method == 'POST':
        if request.POST.get('Register'):
            register_form = CreateUserForm(request.POST)
            if register_form.is_valid():
                register_form.save()

                # Logging in automaticly aflter registration
                username = register_form.cleaned_data['username']
                password = register_form.cleaned_data['password1']
                user = authenticate(request, username = username, password = password)
                login(request, user)
                return redirect('home')
            else:
                print('register fail')
                messages.error(request, 'Registration failed.')

        elif request.POST.get('Login'):
            username = request.POST.get('login_username')
            password = request.POST.get('login_password')
            user = authenticate(request, username = username, password = password)
            print(username + ' ' + password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                print('login fail')
                messages.error(request, 'Login failed.')

    data = {
        'register_form': CreateUserForm,
    }
    return render(request, 'main/login.html', data)

def logout_user(request):
    logout(request)
    return redirect('login_page')

def home(request):
    # If user is not logged in
    if request.user.id == None:
        return redirect('login_page')

    # user = username of logged user
    user = request.user

    # Making the main date changable (currently only with left and right arrow)
    date_change = 0
    if request.POST.get('next'):
        date_change = int(request.POST.get('next')) + 1
    elif request.POST.get('previous'):
        date_change = int(request.POST.get('previous')) - 1
    elif request.POST.get('date_change'): # Used when editing or deleting task (to keep the same date)
        date_change = int(request.POST.get('date_change'))
    date_get = datetime.now() + timedelta(days = date_change)

    # Changing state of the task to opposite
    if request.POST.get('task_done', False) != False:
        task = Task.objects.filter(author = user, id = int(request.POST.get('task_done')))
        if task.first().isDone == True:
            task.update(isDone = False)
        else:
            task.update(isDone = True)
    
    # Adding new task
    if request.POST.get('new_task'):

        task_name = request.POST.get('task_name', 'default')
        task_date = request.POST.get('task_date', datetime.now() )
        date = datetime( int(task_date[0:4]), int(task_date[5:7]), int(task_date[8:10]), int(task_date[11:13]), int(task_date[14:16]))
        new_task = Task(author = user, name = task_name, date = date)
        new_task.save()

        date_get = date # to keep the current page
        date_change = (date - datetime.now()).days + 1 # to sync the days diff

    # Editing task
    if request.POST.get('edit_task', False) != False:
        task = Task.objects.filter(author = user, id = int(request.POST.get('edit_task')))
        task_name = request.POST.get('task_name', 'default')
        task_date = request.POST.get('task_date', datetime.now() )
        date = datetime( int(task_date[0:4]), int(task_date[5:7]), int(task_date[8:10]), int(task_date[11:13]), int(task_date[14:16]))
        task.update(name = task_name, date = date)

        date_get = date # to keep the current page
        date_change = (date - datetime.now()).days + 1 # to sync the days diff
    
    # Deleting task
    if request.POST.get('delete_task', False) != False:
        task = Task.objects.filter(author = user, id = int(request.POST.get('delete_task')))
        task.delete()

    # Getting Tasks from the current day
    '''
    db_data_done = Task.objects.filter(author = user,
                                       isDone = True,
                                       date__day = str(date_get.day),
                                       date__month = str(date_get.month),
                                       date__year = str(date_get.year) ).order_by('date') '''
    db_data_done = Task.objects.raw('SELECT * FROM main_task WHERE \
                                     "author_id" =' + str(user.id) + ' AND "isDone" = True')

    
    db_data_undone = Task.objects.filter(author = user,
                                         isDone = False,
                                         date__day = str(date_get.day),
                                         date__month = str(date_get.month),
                                         date__year = str(date_get.year) ).order_by('date')

    data = {
        'date': date_get,
        'date_change': date_change,
        'db_data_done': db_data_done,
        'db_data_undone': db_data_undone,
        'title': 'Tasks reminder'
    }
    return render(request, 'main/home.html', data)
