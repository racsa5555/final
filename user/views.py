from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .serializers import RegisterSerializer, LogOutSerialzer
from .tasks import send_confirm_email_task, send_password_reset_task


User = get_user_model()

class RegistrationView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                # send_confirmation_email(user.email, user.activation_code)
                send_confirm_email_task.delay(user.email, user.activation_code)
                
            except:
                return Response(
                    {
                        'message': 'Че то не то, на почте нет ниче',
                        'data': serializer.data
                    }, status=HTTPStatus.CREATED
                )
            return Response(serializer.data, status=HTTPStatus.CREATED)
        
class ActivationView(APIView):
    def get(self, request):
        code = request.query_params.get('u')
        user = get_object_or_404(User, activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Активирован', status=HTTPStatus.OK)


class LogoutView(APIView):
    serializer_class = LogOutSerialzer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response('Успешно разлогинилсь', 200)


class CustomResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        user.save()
        if not user:
            return Response({'ValidationError': 'Нет такого пользователя'}, status=HTTPStatus.BAD_REQUEST)
        
        send_password_reset_task.delay(email=email, code=user.activation_code)
        return Response('Вам на почту отправили сообщение', 200)
    


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email','code_confirm', 'new_password', 'password_confirm'],  # Указание обязательных полей
        properties={
            'email':openapi.Schema(type=openapi.TYPE_STRING),
            'code_confirm': openapi.Schema(type=openapi.TYPE_STRING),
            'new_password': openapi.Schema(type=openapi.TYPE_STRING),
            'password_confirm': openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
)
@api_view(['POST'])
def password_confirm(request, *args, **kwargs):
    email = request.data.get('email')
    new_password = request.data.get('new_password')
    password_confirm = request.data.get('password_confirm')
    code = request.data.get('code_confirm')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response('Пользователь не найден', 404)
    
    if user.activation_code != code:
        print(user.activation_code, code)
        return Response(f'Неверный код подтверждения', 400)
    if new_password != password_confirm:
        return Response('Пароли не совпадают', 400)

    user.set_password(new_password)
    user.activation_code = ''
    user.save()

        
