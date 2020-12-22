from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.db import connection # To perform raw sql queries
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
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
                # Saving form
                register_form.save()

                # Logging in automaticly after registration
                username = register_form.cleaned_data['username']
                password = register_form.cleaned_data['password1']
                user = authenticate(request, username = username, password = password)
                login(request, user)

                # Inserting user to Birthdate table
                user_id = request.user.id
                birthdate = register_form.cleaned_data['birthdate']
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO main_birthdate (user_id, birthdate) VALUES ({},date '{}');".format(user_id, birthdate))
                
                return redirect('home')
            else:
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
    user_id = request.user.id

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
    if request.POST.get('task_change_status', False) != False:
        task_id = int(request.POST.get('task_change_status'))
        task = Task.objects.raw("SELECT id, is_done FROM main_task WHERE user_id = {} AND id = {}".format(user_id, task_id))[0]

        if task.is_done == True:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE main_task SET is_done = false WHERE id = {}".format(task_id))
        else:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE main_task SET is_done = true WHERE id = {}".format(task_id))
    
    # Adding new task
    if request.POST.get('new_task'):

        task_name = request.POST.get('task_name', 'default')
        task_date = request.POST.get('task_date', datetime.now() )

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO main_task (name, todo_timestamp, todo_date, user_id)\
                            VALUES ('{}','{}','{}',{});".format(task_name, task_date, task_date, user_id))

        # switch the day to the added task day
        date_get = datetime( int(task_date[0:4]), int(task_date[5:7]), int(task_date[8:10]), int(task_date[11:13]), int(task_date[14:16]))
        date_change = (date_get - datetime.now()).days + 1 # to sync the days diff

    # Editing task
    if request.POST.get('edit_task', False) != False:
        task_id = int(request.POST.get('edit_task'))
        task_name = request.POST.get('task_name', 'default')
        task_date = request.POST.get('task_date', datetime.now())
        
        with connection.cursor() as cursor:
            cursor.execute("UPDATE main_task SET \"name\" = '{}', todo_timestamp = '{}',\
                            todo_date = '{}' WHERE id = {};".format(task_name, task_date, task_date, task_id))

        # switch the day to the added task day
        date_get = datetime( int(task_date[0:4]), int(task_date[5:7]), int(task_date[8:10]), int(task_date[11:13]), int(task_date[14:16]))
        date_change = (date_get - datetime.now()).days + 1 # to sync the days diff
    
    # Deleting task
    if request.POST.get('delete_task', False) != False:
        task_id = int(request.POST.get('delete_task'))
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM main_task WHERE id = {} AND user_id = {}".format(task_id, user_id))

    # Getting Tasks from the current day
    db_data_done = Task.objects.raw("SELECT * FROM main_task WHERE user_id = {} AND todo_date = '{}' AND is_done = true".format(user_id, date_get))
    db_data_undone = Task.objects.raw("SELECT * FROM main_task WHERE user_id = {} AND todo_date = '{}' AND is_done = false".format(user_id, date_get))

    data = {
        'date': date_get,
        'date_change': date_change,
        'db_data_done': db_data_done,
        'db_data_undone': db_data_undone,
        'title': 'Tasks reminder'
    }
    return render(request, 'main/home.html', data)
