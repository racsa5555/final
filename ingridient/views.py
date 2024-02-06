from django.shortcuts import render
from rest_framework.generics import ListAPIView

from dish.models import IngridientItem
from dish.serializers import IngridientItemSerializer

from .models import Ingridient

# class IngridientViewSet(CreateAPIView):

#     def post(self, request, *args, **kwargs):
#         data = request.data
#         ingridients_id = (i['ingridient'] for i in data['ingridients'])
#         items = IngridientItem.objects.all()
#         for x in items:
 
#         pass
class IngridientItemAPIView(ListAPIView):
    serializer_class = IngridientItemSerializer

    def get_queryset(self):
        queryset = IngridientItem.objects.all()
        return queryset
    

    
