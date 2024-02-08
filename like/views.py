from rest_framework.generics import ListAPIView

from .serializers import LikeHistorySerializer, LikeSerializer
from .models import Like


class LikeHistoryAPIView(ListAPIView):
    serializer_class = LikeHistorySerializer
    queryset = Like.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = Like.objects.select_related('owner').filter(owner=user)
        return queryset
