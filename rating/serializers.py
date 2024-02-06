from rest_framework import serializers
from rating.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.email')
    dish = serializers.ReadOnlyField(source = 'dish.name')

    class Meta:
        model = Rating
        fields = '__all__'