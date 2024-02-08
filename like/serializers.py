from rest_framework import serializers

from .models import Favorite,Like


class FavoriteSerializer(serializers.Serializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    dish = serializers.ReadOnlyField(source='dish.name')

    class Meta:
        fields = '__all__'
        model = Favorite
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        return repr['dish']
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class LikeHistorySerializer(serializers.ModelSerializer):
    dish = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = '__all__'

    def get_dish(self,obj):
        return obj.dish.name