from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


start_kb = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Регистрация',callback_data='register')],
        [InlineKeyboardButton(text = 'Вход',callback_data='login')],
        [InlineKeyboardButton(text = 'Информация',callback_data='info')]    
    ]
)

activate_kb = InlineKeyboardBuilder(
    markup=[[InlineKeyboardButton(text = "Все,я активировал",callback_data='activate')]]
)