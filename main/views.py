from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.db import connection # To perform raw sql queries
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
from .row_sql_dict import dictfetchall

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
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Login failed.')

    data = {
        'register_form': CreateUserForm,
        'title': 'Tasks reminder - login'
    }
    return render(request, 'main/login.html', data)

def logout_user(request):
    logout(request)
    return redirect('login_page')

def home(request):
    # If user is not logged in
    if request.user.id is None:
        return redirect('login_page')

    # user = username of logged user
    user = request.user
    user_id = request.user.id

    # Making the main date changable (currently only with left and right arrow)
    if request.POST.get('date_change'): # Used when editing or deleting task (to keep the same date)
        date_change = int(request.POST.get('date_change'))
    else:
        date_change = 0
    date_get = datetime.now() + timedelta(days = date_change)

    # Changing state of the task to opposite
    if request.POST.get('task_change_status', False) != False:
        task_id = int(request.POST.get('task_change_status'))

        with connection.cursor() as cursor:
            cursor.execute("UPDATE main_task SET is_done = NOT is_done WHERE id = {id}".format(id = task_id))

    # Adding new task
    if request.POST.get('new_task'):

        task_name = request.POST.get('task_name', 'default')
        task_date = request.POST.get('task_date', datetime.now() )

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO main_task (name, todo_timestamp, todo_date, user_id)\
                            VALUES ('{}','{}','{}',{});".format(task_name, task_date, task_date, user_id))

        # switch the day to the added task day
        date_get = datetime( int(task_date[0:4]), int(task_date[5:7]), int(task_date[8:10]), int(task_date[11:13]), int(task_date[14:16]))
        date_change = (date_get - datetime.now()).days + 1 # keep the date with todo_date of added task

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
        date_change = (date_get - datetime.now()).days # keep the date with todo_date of edited task
    
    # Deleting task
    if request.POST.get('delete_task', False) != False:
        task_id = int(request.POST.get('delete_task'))
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM main_task WHERE id = {} AND user_id = {}".format(task_id, user_id))

    # Sharing task
    # TODO: synchronizowac date sharowanego z akutualną (zmienia na dzisiejszą)
    if request.POST.get('share_task', False) != False:
        task_id = int(request.POST.get('share_task'))
        friend_name = request.POST.get('share_user')

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO main_share (task_id, friendship_id) \
                            VALUES ({}, (SELECT f.id FROM main_friends f, auth_user u \
                            WHERE f.user1_id = {} AND f.user2_id = u.id AND u.username = '{}'));".format(task_id, user_id, friend_name))

    # Sharing delete for all users
    if request.POST.get('share_delete_all', False) != False:
        task_id = int(request.POST.get('share_delete_all'))

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM main_share WHERE task_id = {} \
                            AND task_id IN (SELECT id FROM main_task WHERE user_id = {});".format(task_id, user_id))

    # Sharing delete
    if request.POST.get('share_delete', False) != False:
        share_id = int(request.POST.get('share_delete'))

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM main_share WHERE id = {} AND friendship_id = \
                            (SELECT id FROM main_friends WHERE user2_id = {});".format(share_id, user_id))      

    # Getting data from database
    with connection.cursor() as cursor:
        # Getting Tasks from the current day
        cursor.execute("SELECT * FROM main_task WHERE user_id = {} AND todo_date = '{}' AND is_done = true ORDER BY todo_timestamp".format(user_id, date_get))
        db_data_done = dictfetchall(cursor)
        cursor.execute("SELECT * FROM main_task WHERE user_id = {} AND todo_date = '{}' AND is_done = false ORDER BY todo_timestamp".format(user_id, date_get))
        db_data_undone = dictfetchall(cursor)

        # Getting shared tasks from the current day
        cursor.execute("SELECT s.id, t.name, t.todo_timestamp, u.username FROM main_task t, auth_user u, main_friends f, main_share s\
                        WHERE s.friendship_id = f.id AND f.user2_id = {} AND u.id = f.user1_id AND s.task_id = t.id AND t.todo_date = '{}' AND t.is_done = true \
                        ORDER BY t.todo_timestamp".format(user_id, date_get))
        shared_done = dictfetchall(cursor)

        cursor.execute("SELECT s.id, t.name, t.todo_timestamp, u.username FROM main_task t, auth_user u, main_friends f, main_share s\
                        WHERE s.friendship_id = f.id AND f.user2_id = {} AND u.id = f.user1_id AND s.task_id = t.id AND t.todo_date = '{}' AND t.is_done = false \
                        ORDER BY t.todo_timestamp".format(user_id, date_get))
        shared_undone = dictfetchall(cursor)
        
        # Friend nicknames
        cursor.execute("SELECT u.username FROM auth_user u\
                        WHERE (u.id IN (SELECT user2_id FROM main_friends WHERE user1_id = '{u_id}' AND is_accepted = true)\
                        OR u.id IN (SELECT user1_id FROM main_friends WHERE user2_id = '{u_id}' AND is_accepted = true))".format(u_id = user_id))
        friend_nick = cursor.fetchall()

        # Friend's birthday
        cursor.execute("SELECT u.username FROM auth_user u, main_birthdate b \
                        WHERE (u.id IN (SELECT user2_id FROM main_friends WHERE user1_id = '{u_id}' AND is_accepted = true)\
                        OR u.id IN (SELECT user1_id FROM main_friends WHERE user2_id = '{u_id}' AND is_accepted = true))\
                        AND u.id = b.user_id AND CAST(b.birthdate as text) ~ '{date}'".format(u_id = user_id, date = str(date_get)[4:10]))
        friend_bday = cursor.fetchall()

    data = {
        'date': date_get,
        'date_change': date_change,
        'db_data_done': db_data_done,
        'shared_done' : shared_done,
        'shared_undone' : shared_undone,
        'db_data_undone': db_data_undone,
        'friend_nick' : friend_nick,
        'friend_bday' : friend_bday,
        'title': 'Tasks reminder - home'
    }
    return render(request, 'main/home.html', data)

def friends(request):
    # If user is not logged in
    if request.user.id is None:
        return redirect('login_page')

    user_id = request.user.id

    if request.method == 'POST':
        
        if request.POST.get('friend_add'):
            friend_id = "SELECT id FROM auth_user WHERE username = '{}'".format(request.POST.get('friend_name'))
                          
            with connection.cursor() as cursor:
                cursor.execute('SELECT id FROM main_friends \
                                WHERE (user1_id = {id1} AND user2_id = ({id2})) \
                                OR (user1_id = ({id2}) AND user2_id = {id1})'.format(id1 = user_id, id2 = friend_id))
                if len(cursor.fetchall()) == 0: # Checking if two accounts are not already in freinds table
                    cursor.execute("INSERT INTO main_friends (user1_id, user2_id)\
                                    VALUES ({}, ({}));".format(user_id, friend_id))

        if request.POST.get('friend_delete'):
            friend_id = "SELECT id FROM auth_user WHERE username = '{}'".format(request.POST.get('friend_delete'))
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM main_friends WHERE (user1_id = {id1} AND user2_id = ({id2})) OR\
                                (user1_id = ({id2}) AND user2_id = {id1});".format(id1 = user_id, id2 = friend_id))

        if request.POST.get('friend_accept'):
            friend_id = "SELECT id FROM auth_user WHERE username = '{}'".format(request.POST.get('friend_accept'))
            with connection.cursor() as cursor:
                cursor.execute("UPDATE main_friends SET is_accepted = true \
                                WHERE user1_id = ({f_id}) AND user2_id = {u_id};\
                                INSERT INTO main_friends (user1_id, user2_id, is_accepted)\
                                VALUES ({u_id}, ({f_id}), true);".format(f_id = friend_id, u_id = user_id))

    # Getting data from the database
    with connection.cursor() as cursor:
        # Friend request sent to user
        cursor.execute("SELECT username FROM auth_user WHERE id IN (SELECT user1_id FROM main_friends WHERE user2_id = '{}' AND is_accepted = false)".format(user_id))
        friends_request = dictfetchall(cursor)

        # Friend request sent by user
        cursor.execute("SELECT username FROM auth_user WHERE id IN (SELECT user2_id FROM main_friends WHERE user1_id = '{}' AND is_accepted = false)".format(user_id))
        friends_pending = dictfetchall(cursor)

        # Accepted friend
        cursor.execute("SELECT u.username, b.birthdate FROM auth_user u, main_birthdate b \
                        WHERE (u.id IN (SELECT user2_id FROM main_friends WHERE user1_id = '{u_id}' AND is_accepted = true)\
                        OR u.id IN (SELECT user1_id FROM main_friends WHERE user2_id = '{u_id}' AND is_accepted = true))\
                        AND u.id = b.user_id".format(u_id = user_id))
        friends = dictfetchall(cursor)

    data = {
        'friends_request': friends_request,
        'friends_pending': friends_pending,
        'friends': friends,
        'title': 'Tasks reminder - friends'
    }
    return render(request, 'main/friends.html', data)
