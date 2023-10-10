from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
# Create your views here.


def login(request):

    if request.session.get('user_id', None) is not None:
        return redirect('/')

    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            request.session['user_id'] = user.id
            return JsonResponse({'success': 'True'}, safe=False)
        return JsonResponse({'success': 'False'}, safe=False)
        
    return render(request, 'user/login.html')


def signup(request):

    if request.session.get('user_id', None) is not None:
        return redirect('/')

    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)

        if username is None or password is None:
            return JsonResponse({'success': 'False'}, safe=False)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': 'username'}, safe=False)
        
        User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return JsonResponse({'success': 'True'}, safe=False)
    return render(request, 'user/signup.html')


def logout(request):

    if request.session.get('user_id', None) is not None:
        del request.session['user_id']
    return redirect('/user/login')
