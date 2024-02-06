from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    dish = serializers.ReadOnlyField(source='dish.name')

    class Meta:
        exclude = ['id']
        model = Comment
