from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="todo"),
    path("add/", views.add, name="add_todo"),
    path("edit/<int:todo_id>/", views.edit, name="edit_todo"),
    path("delete/", views.delete, name="delete_all"),
    path("show/", views.show, name="show_all"),
]
