from rest_framework import serializers
from .models import Ingridient


class IngridientGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingridient
        fields = ['id','name']
