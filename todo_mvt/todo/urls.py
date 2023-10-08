from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="todo"),
    path("add/", views.add, name="add_todo"),
    path("edit/<int:id>/", views.edit, name="edit_todo"),
    path("delete/<int:id>", views.delete, name="delete_all"),
]
