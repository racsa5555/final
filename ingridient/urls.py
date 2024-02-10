from django.urls import path, include

from .views import *

urlpatterns = [
    path('',IngridientItemAPIView.as_view()),
    path('get/',IngridientsGetSerializer.as_view())
]
