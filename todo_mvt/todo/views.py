from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Todo
from datetime import datetime
# Create your views here.


def index(request):
    if not request.session.get('user_id', None):
        return redirect('/user/login')

    flag = request.GET.get('flag', None)

    if not flag:
        data = Todo.objects.filter(
            user=request.session['user_id']
        ).all()

    elif flag == "completed":
        data = Todo.objects.filter(
            user=request.session['user_id'],
            is_completed=True
        ).all()

    elif flag == "pending":
        data = Todo.objects.filter(
            user=request.session['user_id'],
            is_completed=False,
            expiry__gte=datetime.now()
        ).all()

    elif flag == "expired":
        data = Todo.objects.filter(
            user=request.session['user_id'],
            is_completed=False,
            expiry__lt=datetime.now()
        ).all()
    return render(request, "todo/index.html", {'data': data})


def add(request):

    if not request.session.get('user_id', None):
        return redirect('/user/login')
    
    if request.method == "POST":
        title = request.POST.get('title', None)
        expiry = request.POST.get('expiry', None)

        if title is None or expiry is None:
            return render(
                request, 'todo/add.html',
                {'error': 'Invalid title or expiry'}
            )
        Todo.objects.create(
            title=title,
            expiry=expiry,
            user=User.objects.get(pk=request.session['user_id'])
        )
        return redirect("/")
    return redirect("/todo/add.html")

def edit_helper(user, todo_ids, title, expiry, is_completed):

    todo = Todo.objects.filter(pk__in=todo_ids, user=user)
    todo.update(
        title = todo.title if title is None else title,
        expiry = todo.expiry if expiry is None else expiry,
        is_completed = todo.is_completed if is_completed is None else is_completed
    )

def edit(request, id = None):
    if not request.session.get('user_id', None):
        return redirect('/user/login')
    
    if request.method == "POST":
        user = User.objects.get(pk=request.session['user_id'])
        title = request.POST.get('title', None)
        expiry = request.POST.get('expiry', None)
        is_completed = request.POST.get('is_completed', None)
        todo_ids = request.POST.get('ids', None)

        if title is None or expiry is None or is_completed is None:
            return render(
                request, 'todo/edit.html',
                {'error': 'Data not given properly'}
            )
        if id:
            edit_helper(user, [id], title, expiry, is_completed)
            return redirect("/")
        
        if todo_ids is None:
            return render(
                request, 'todo/edit.html',
                {'error': 'No todos selected'}
            )
        edit_helper(user, todo_ids, title, expiry, is_completed)
        return redirect("/")



def delete(request, id = None):

    if request.session.get('user_id', None) is None:
        return redirect('/user/login')
    
    if request.method=='POST':
        flag = request.POST.get('flag', None)
        user = User.objects.get(pk=request.session['user_id'])
        selected = request.POST.get('selected', None)
        if id:
            Todo.objects.filter(pk=id, user=user).delete()

        if not flag:
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
                return render(
                    request, 'todo/delete.html',
                    {'error': 'No todos selected'}
                )
            Todo.objects.filter(
                user=user, 
                pk__in=selected
            ).delete()
    
        return redirect('/')



