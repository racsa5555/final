from rest_framework.generics import ListAPIView

from .serializers import LikeHistorySerializer,FavoriteHistorySerializer
from .models import Like, Favorite


class LikeHistoryAPIView(ListAPIView):
    serializer_class = LikeHistorySerializer
    queryset = Like.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = Like.objects.select_related('owner').filter(owner=user)
        return queryset


class FavoriteHistoryAPIView(ListAPIView):
    serializer_class = FavoriteHistorySerializer
    queryset = Favorite.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = Favorite.objects.select_related('owner').filter(owner=user)
        return queryset
