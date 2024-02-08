from django.shortcuts import render
from rest_framework.generics import ListAPIView

from dish.models import IngridientItem
from dish.serializers import IngridientItemSerializer


class IngridientItemAPIView(ListAPIView):
    serializer_class = IngridientItemSerializer

    def get_queryset(self):
        queryset = IngridientItem.objects.all()
        return queryset
    

    
