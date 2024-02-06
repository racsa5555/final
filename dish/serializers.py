from ingridient.models import Ingridient
from rest_framework import serializers
from django.db.models import Avg,Count

from .models import Dish,IngridientItem
from comment.models import Comment
from comment.serializers import CommentSerializer
from like.models import Like

class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingridient


class IngridientItemSerializer(serializers.ModelSerializer):
    ingridient = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    class Meta:
        fields = ['ingridient','quantity','id']
        model = IngridientItem
    def get_id(self,obj):
        id = obj.ingridient.id
        return id
    def get_ingridient(self,obj):
        name = obj.ingridient.name
        return name


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
    

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['ingridients'] = IngridientItemSerializer(instance.items.all(),many = True).data
        action = self.context.get('view')
        if action == 'retrieve':
            comments = Comment.objects.filter(dish = instance)
            rep['comments'] = CommentSerializer(comments,many=True).data
            rep['rating'] = instance.rating.aggregate(Avg('rating'))
            rating = rep['rating']
            rating['rating_count'] = instance.rating.count()
            rep['likes_count'] = Like.objects.filter(dish=instance).count()
        return rep
    


