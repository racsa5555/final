from django.core.mail import send_mail
from django.utils.html import format_html

def send_confirmation_email(email, code):
    activation_url = f'http://localhost:8000/user/activate/?u={code}'
    message = format_html(
        'Здравствуйте, активируйте ваш аккаунт'
        'Чтобы активировать аккаунт, перейдите по ссылке'
        '<br>'
        '<a href= "{}">{}</a>'
        '<br>'
        'Не передавайте код никому',
        activation_url, activation_url
    )
    
    send_mail(
        'Здравствуйте',
        message,
        'test@gmail.com',
        [email],
        fail_silently=False
    )


def send_password_reset_email(email, user_id):
    password_reset_url = f'http://localhost:8000/account/password_confirm/{user_id}'
    message = format_html(
        'Здравствуйте, чтобы восстановить пароль вам нужно перети по ссылке'
        '<br>'
        '<a href= "{}">{}<\a>'
        '<\br>',
        password_reset_url, password_reset_url
    )


    send_mail(
        'Здравствуйте',
        message,
        'test@gmail.com',
        [email],
        fail_silently=False
    )