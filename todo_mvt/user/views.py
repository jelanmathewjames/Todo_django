from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# Create your views here.


def login(request):

    if request.session.get('user_id', None) is not None:
        return redirect('/')

    if request.method == "POST":
        username = request.POST('username', None)
        password = request.POST('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            request.session['user_id'] = user.id
            return redirect('/')
        return render(request, 'user/login.html', {'error': 'Invalid username or password'})
    return render(request, 'user/login.html')


def signup(request):

    if request.session.get('user_id', None) is not None:
        return redirect('/')

    if request.method == "POST":
        username = request.POST('username', None)
        password = request.POST('password', None)
        first_name = request.POST('first_name', None)
        last_name = request.POST('last_name', None)

        if username is None or password is None:
            return render(
                request, 'user/signup.html',
                {'error': 'Invalid username or password'}
            )

        User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return redirect('/user/login')
    return render(request, 'user/signup.html')


def logout(request):

    if request.session.get('user_id', None) is not None:
        del request.session['user_id']
    return redirect('/user/login')
