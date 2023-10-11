from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Todo
from datetime import datetime
from django.db.models import Case, When, Value, CharField
from pytz import timezone
# Create your views here.


def index(request):
    if not request.session.get('user_id', None):
        return redirect('/user/login')

    flag = request.GET.get('flag', None)
    zone = timezone('Asia/Kolkata')
    data = Todo.objects.annotate(status=Case(
                When(is_completed=True, then=Value("completed")),
                When(expiry__lt=datetime.now(zone), then=Value("expired")),
                When(expiry__gte=datetime.now(zone), then=Value("pending")),
                output_field=CharField()
            )
        )
    if not flag:
        data =  data.filter(user=request.session['user_id']).all()

    elif flag == "completed":
        data = data.filter(
            user=request.session['user_id'],
            is_completed=True
        ).all()

    elif flag == "pending":
        data = data.filter(
            user=request.session['user_id'],
            is_completed=False,
            expiry__gte=datetime.now()
        ).all()

    elif flag == "expired":
        data = data.filter(
            user=request.session['user_id'],
            is_completed=False,
            expiry__lt=datetime.now()
        ).all()
    return render(request, "todo/index.html", {'data': data, 'current': datetime.now()})


def create(request):

    if not request.session.get('user_id', None):
        return redirect('/user/login')
    
    if request.method == "POST":
        title = request.POST.get('title', None)
        expiry = request.POST.get('expiry', None)
        if title is None or expiry is None:
            return JsonResponse({'success': 'False'}, safe=False)
        
        Todo.objects.create(
            title=title,
            expiry=expiry,
            user=User.objects.get(pk=request.session['user_id'])
        )
        return JsonResponse({'success': 'True'}, safe=False)
    return render(request, "todo/add.html")
    
def edit(request):
    if not request.session.get('user_id', None):
        return redirect('/user/login')
    
    if request.method == "POST":
        user = User.objects.get(pk=request.session['user_id'])
        Todo.objects.filter(
            is_completed=False, 
            user=user, 
            expiry__gte=datetime.now()
        ).all().update(is_completed=True)

        return JsonResponse({'success': 'True'}, safe=False)

def edit_id(request, id = None):

    if not request.session.get('user_id', None):
        return redirect('/user/login')
    
    if request.method == 'POST':
        user = User.objects.get(pk=request.session['user_id'])
        title_ = request.POST.get('title', None)
        expiry_ = request.POST.get('expiry', None)
        is_completed_ = request.POST.get('is_completed', None)
        
        todo = Todo.objects.filter(pk=id, user=user).first()
        todo.title = title_ if title_ is not None else todo.title
        todo.expiry = expiry_ if expiry_ is not None else todo.expiry
        todo.is_completed = True if is_completed_ == 'true' else todo.is_completed
        todo.save()

        return JsonResponse({'success': 'True'}, safe=False)

def delete(request):
    if request.session.get('user_id', None) is None:
        return redirect('/user/login')
    
    if request.method=='POST':
        flag = request.POST.get('flag', None)
        user = User.objects.get(pk=request.session['user_id'])
        selected = request.POST.get('selected', None)
        id = request.POST.get('id', None)
        if id:
            Todo.objects.filter(pk=id, user=user).delete()

        elif flag == 'all':
            Todo.objects.filter(user=user).delete()

        elif flag == 'completed':
            Todo.objects.filter(
                user=user, 
                is_completed=True
            ).delete()

        elif flag == 'pending':
            Todo.objects.filter(
                user=user, 
                is_completed=False, 
                expiry__gte=datetime.now()
        ).delete()
        
        elif flag == 'expired':
            Todo.objects.filter(
                user=user, 
                is_completed=False, 
                expiry__lt=datetime.now()
            ).delete()
        
        elif flag == 'selected':
            if selected is None:
                return JsonResponse({'success': 'False'}, safe=False)
            Todo.objects.filter(
                user=user, 
                pk__in=selected
            ).delete()
        else:
            return JsonResponse({'success': 'False'}, safe=False)
        return JsonResponse({'success': 'True'}, safe=False)



