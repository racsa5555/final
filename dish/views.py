from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Dish
from .serializers import *
from ingridient.models import Ingridient


class DishViewSet(ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()
    
    def list(self, request, *args, **kwargs):
        serializers = self.serializer_class(self.queryset,many = True)
        return Response(serializers.data)

class YouCanCook(ListCreateAPIView):
    serializer_class = DishSerializer

    def list(self, request, *args, **kwargs):
        queryset = Ingridient.objects.all()
        serializer = IngridientSerializer(queryset,many = True)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        data = request.data
        
