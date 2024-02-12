from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from like.models import Favorite, Like
from comment.serializers import CommentSerializer
from rating.serializers import RatingSerializer

from .models import Dish
from .fiters import DishFilter
from .serializers import *
from .permissions import IsOwner



class DishPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'



class DishViewSet(ModelViewSet):
    queryset = Dish.objects.prefetch_related('ingridients')
    pagination_class = DishPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = DishFilter
    search_fields = ['name']
    
    def get_permissions(self):
        if self.request.method in ('PATCH', 'PUT', 'DELETE'):
            return [IsAuthenticated(), IsOwner()]
        return [AllowAny()]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DishRetrieveSerializer
        return DishSerializer
    
    @swagger_auto_schema(method='POST', request_body=CommentSerializer, operation_description='add comment for post')
    @action(detail=True, methods=['POST'])
    def comment(self, request, pk=None):
        dish = self.get_object()
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(dish=dish, owner=request.user)
        return Response('успешно добавлено', 201)
    
    @action(['GET','POST','PATCH','DELETE'],detail=True)
    def rating(self,request,pk):
        dish = self.get_object()
        user = request.user

        if request.method == 'GET':
            ratings = dish.rating.all()
            serializer = RatingSerializer(instance = ratings,many = True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = RatingSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner = user,dish = dish)
            return Response(serializer.data,201)
        elif request.method in ['PUT','PATCH']:
            if not dish.rating.filter(owner = user).exists():
                return Response('You dont post rating',400)
            rating = dish.rating.get(owner = user)
            serializer = RatingSerializer(rating,data = request.data,partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,200)
        else:
            if not dish.rating.filter(owner = user).exists():
                return Response('You dont post rating',400)
            rating = dish.rating.get(owner = user)
            rating.delete()
            return Response('Удалено',204)
        
    @action(detail=True, methods=['POST'])
    def toggle_like(self, request, pk=None):
        dish = self.get_object()
        like = request.user.likes.filter(dish=dish)
        if like:
            like.delete()
            return Response('успешно удалено', 204)
        like = Like.objects.create(
            dish=dish,
            owner=request.user
        )
        return Response('успешно добавлено', 201)

    @action(detail=True, methods=['POST'])
    def toggle_favorite(self, request, pk=None):
        dish = self.get_object()
        favorite = request.user.favorites.filter(dish=dish)
        if favorite:
            favorite.delete()
            return Response('удалено из избранных', 204)
        favorite = Favorite.objects.create(
            dish=dish,
            owner=request.user
        )
        return Response('добавлено в избранное', 201)
    
    @action(detail = False, methods = ['GET'],permission_classes=[IsAuthenticated()])
    def recomendations(self,request):
        pass

        





