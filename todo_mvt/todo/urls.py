from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="todo"),
    path("create", views.create, name="create_todo"),
    path("edit/<int:id>", views.edit_id, name="edit_todo"),
    path("edit", views.edit, name="delete_todo"),
    path("delete", views.delete, name="delete_todo"),
]
