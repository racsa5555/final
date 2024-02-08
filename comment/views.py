from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response


from .serializers import CommentSerializer
from .models import Comment
from .permissions import IsOwner

class StandartResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = StandartResultPagination

    @action(detail=False, methods=['GET'])
    def get_user_comments(self, request):
        user_comments = Comment.objects.select_related('owner').filter(owner = request.user)
        serializer = CommentSerializer(user_comments, many=True)
        return Response(serializer.data)


    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated(), IsOwner()]
        return [permissions.AllowAny()]



    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    

