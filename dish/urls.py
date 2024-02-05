from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register('',DishViewSet)

urlpatterns = [
    path('my_ingr/',YouCanCook.as_view()),
    path('',include(router.urls)),
    
    
]