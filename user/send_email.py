from django.core.mail import send_mail
from django.utils.html import format_html

def send_confirmation_email(email, code):
    activation_url = f'http://34.16.110.19/api/user/activate/?u={code}'
    message = format_html(
        'Здравствуйте, активируйте ваш аккаунт'
        'Чтобы активировать аккаунт, перейдите по ссылке '
        ' {} '
        'Не передавайте код никому',
        activation_url
    )
    
    send_mail(
        'Здравствуйте',
        message,
        'test@gmail.com',
        [email],
        fail_silently=False
    )


def send_password_reset_email(email, code):
    password_reset_url = f'{code}'
    message = format_html(
        'Здравствуйте, Ваш код подтверждения:'
        ' {} ',
        password_reset_url
    )


    send_mail(
        'Здравствуйте',
        message,
        'test@gmail.com',
        [email],
        fail_silently=False
    )