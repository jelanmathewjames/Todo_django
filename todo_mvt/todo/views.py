from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, "todo/index.html")

def add(request):
    return redirect("/")

def edit(request):
    return render(request, "todo/edit.html")

def delete(request):   
    return render(request, "todo/delete.html")

def show(request):
    return render(request, "todo/show.html")



