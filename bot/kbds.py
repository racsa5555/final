from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks import RatingCallback


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

dish_kb = InlineKeyboardBuilder(
    markup =[
        [InlineKeyboardButton(text = 'Посмотреть блюда',callback_data = 'get_dishes')],
    ]
)

next_or_stop_dish = InlineKeyboardBuilder(
    markup =[
        [
        InlineKeyboardButton(text = 'Следющее блюдо',callback_data = 'next_dish'),
        InlineKeyboardButton(text = 'Стоп',callback_data = 'stop_dish'),
        ]
    ]
)


def rating_kb(id):
    rating_kb = InlineKeyboardBuilder()
    for x in range(1,6):
        rating_kb.button(text=str(x), callback_data=RatingCallback(dish =id, rating = x,action = 'save'))
    return rating_kb.as_markup()
