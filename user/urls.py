from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from like.views import LikeHistoryAPIView,FavoriteHistoryAPIView

from .views import *

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('like_history/', LikeHistoryAPIView.as_view()),
    path('favorite_history/', FavoriteHistoryAPIView.as_view()),
    path('forgot_password/', CustomResetPasswordView.as_view()),
    path('forgot_password_confirm/', password_confirm)
]

