from django.shortcuts import render
from rest_framework.generics import ListAPIView

from dish.models import IngridientItem
from dish.serializers import IngridientItemSerializer
from ingridient.models import Ingridient

from .serializers import IngridientGetSerializer


class IngridientItemAPIView(ListAPIView):
    serializer_class = IngridientItemSerializer

    def get_queryset(self):
        queryset = IngridientItem.objects.all()
        return queryset
    

class IngridientsGetSerializer(ListAPIView):
    serializer_class = IngridientGetSerializer
    queryset = Ingridient.objects.all()
