from rest_framework.routers import DefaultRouter
from .views import TodoViewSet
from django.urls import path, include
router = DefaultRouter(trailing_slash=False)
router.register('todos', TodoViewSet, basename='todos')

urlpatterns = router.urls

urlpatterns = [
    path(r"", include(router.urls)),
]