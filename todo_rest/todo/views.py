from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
# Create your views here.

class TodoViewSet(ViewSet):
    
    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

    @action(detail=False, methods=['GET'])
    def completed(self, request):
        pass

    @action(detail=False, methods=['GET'])
    def pending(self, request):
        pass

    @action(detail=False, methods=['GET'])
    def expired(self, request):
        pass
