from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from like.views import LikeHistoryAPIView

from .views import *

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('reset_password/', CustomResetPasswordView.as_view()),

    path('password_confirm/<uidb64>/', CustomPasswordConfirmView.as_view()),
    path('like_history/', LikeHistoryAPIView.as_view())
]