from rest_framework import serializers
from django.db.models import Avg

from ingridient.models import Ingridient
from comment.models import Comment
from comment.serializers import CommentSerializer
from like.models import Like
from .models import Dish,IngridientItem

class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingridient


class IngridientItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['ingridient','quantity','id']
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
    
class DishRetrieveSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Dish
        fields = '__all__'

    def get_comments(self,obj):
        comments = Comment.objects.select_related('dish').filter(dish = obj)
        return CommentSerializer(comments,many=True).data
    
    def get_likes_count(self,obj):
        return Like.objects.select_related('dish').filter(dish=obj).count()
    
    
    def get_rating(self,obj):
        return obj.rating.aggregate(Avg('rating'))
    
    def get_rating_count(self,obj):
        return obj.rating.count()
    
    