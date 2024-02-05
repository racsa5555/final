from .models import Dish,IngridientItem
from ingridient.models import Ingridient
from rest_framework import serializers

class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingridient


class IngridientItemSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['dish','id']
        model = IngridientItem


class DishSerializer(serializers.ModelSerializer):
    ingridients = IngridientItemSerializer(many = True,write_only = True)
    type = serializers.CharField()
    owner = serializers.ReadOnlyField(source = 'user.email')
    cuisine = serializers.CharField()

    class Meta:
        model = Dish
        fields = '__all__'

    def create(self, validated_data):
        ingridients = validated_data.pop('ingridients')
        request = self.context.get('request')
        user = request.user
        dish = Dish.objects.create(owner = user,**validated_data)
        for ingridient in ingridients:
            try:
                IngridientItem.objects.create(dish = dish,ingridient = ingridient['ingridient'],quantity = ingridient['quantity'])
            except:
                IngridientItem.objects.create(dish = dish,ingridient = ingridient['ingridient'])
        return dish
    
    