import asyncio

from aiogram import Bot, Dispatcher,types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from decouple import config
from magic_filter import F

from kbds import activate_kb,start_kb,dish_kb,next_or_stop_dish,rating_kb
from pretty_response import pretty_dish
from states import *
from send_requests import *
from callbacks import RatingCallback


TOKEN = config('BOT_TOKEN')


bot = Bot(TOKEN)

dp = Dispatcher()


dishes_generator = None
id = None



@dp.message(CommandStart())
async def start_command(message:types.Message):
    await message.answer(text = 'Приветствую тебя в боте Goodzy',reply_markup=start_kb.as_markup())


@dp.callback_query(lambda query: query.data == 'login')
async def login_user(query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(chat_id = query.message.chat.id,message_id=query.message.message_id)
    await state.update_data(login = True)
    await state.set_state(UserRegisterState.email)
    await query.message.answer(text = 'Введите ваш email')


@dp.callback_query(lambda query: query.data == 'register')
async def register_user(query: types.CallbackQuery, state: FSMContext)-> None:
    await bot.edit_message_reply_markup(chat_id = query.message.chat.id,message_id=query.message.message_id)
    await state.set_state(UserRegisterState.email)
    await query.message.answer(text = 'Введите ваш email')
        

@dp.message(UserRegisterState.email)
async def set_user_email(message: types.Message,state: FSMContext):
    if '@' not in message.text:
        await message.answer(f'Братишка это не почта')
    else:
        await state.update_data(email=message.text)
        data = await state.get_data()
        if data.get('login'):
            await state.set_state(UserRegisterState.password)
            await message.answer(text = 'Введите пароль')
        else:
            await state.set_state(UserRegisterState.first_name)
            await message.answer(f'Введите имя')


@dp.message(UserRegisterState.first_name)
async def set_user_first_name(message: types.Message,state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(UserRegisterState.last_name)
    await message.answer(f'Введите фамилию')


@dp.message(UserRegisterState.last_name)
async def set_user_last_name(message: types.Message,state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(UserRegisterState.password)
    await message.answer(f'Придумайте пароль')

@dp.message(UserRegisterState.password)
async def set_user_pasword(message: types.Message,state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    if data.get('login'):
        user = User(data)
        if await user.login_api():
            await state.update_data(user=user)
            await message.answer(text = 'Вы успешно вошли в аккаунт',reply_markup = dish_kb.as_markup())
        else:
            await message.answer(text = 'Неверный пароль, попробуйте еще раз')
    else:
        data["password_confirm"] = data["password"]
        user = User(data)
        await state.update_data(user=user)
        res = await user.register_api()
        if "email" not in res:
            await message.answer(text = str(res),reply_markup=activate_kb.as_markup())
        else:
            await message.answer(text = str(res))

@dp.callback_query(lambda query: query.data == 'activate')
async def user_activated(query :types.CallbackQuery,state:FSMContext):
    user_data = await state.get_data() 
    user = user_data.get('user')
    await bot.edit_message_reply_markup(chat_id = query.message.chat.id,message_id=query.message.message_id)
    res = await user.login_api()
    if not res:
        await query.message.answer(text='Братишка, ты еще не активировал',reply_markup=activate_kb.as_markup())
    else:
        await query.message.answer(text="Вы успешно активировали аккаунт, и вошли в систему",reply_markup = dish_kb.as_markup())
    

@dp.callback_query(lambda query: query.data == 'get_dishes')
async def get_dishes(query:types.CallbackQuery,state:FSMContext):
    user_data = await state.get_data()
    user = user_data.get('user')
    response = await user.get_dishes()
    global dishes_generator
    global id
    dishes_generator = pretty_dish(response)
    dish_text,id = next(dishes_generator)
    rating_callback = RatingCallback(dish=id, rating=0,action = 'res')  
    await query.message.answer(text = dish_text,reply_markup = next_or_stop_dish.button(text = 'Поставить рейтинг',callback_data=rating_callback).as_markup())

@dp.callback_query(lambda query: query.data == 'next_dish')
async def next_dish(query:types.CallbackQuery):
    global dishes_generator
    global id
    if dishes_generator:
        try:
            dish_text,id = next(dishes_generator)
            await query.message.answer(text = dish_text, reply_markup=next_or_stop_dish.as_markup())
        except StopIteration:
            await query.answer(text="Блюда закончились",reply_markup=dish_kb.as_markup())


@dp.callback_query(RatingCallback.filter(F.action == 'res'))
async def rating(callback: types.CallbackQuery, 
        callback_data: RatingCallback):
    global id
    await callback.message.answer(text = 'Какой рейтинг вы хотите поставить блюду?',reply_markup=rating_kb(id))


@dp.callback_query(RatingCallback.filter(F.action == 'save'))
async def set_rating(callback: types.CallbackQuery, 
        callback_data: RatingCallback,state:FSMContext):
    global id
    user_data = await state.get_data()
    user = user_data.get('user')
    res = await user.rating(callback_data.dish,callback_data.rating)
    await callback.message.answer(text = f'Оценка {callback_data.rating} блюду c id = {id} удачно поставлена')
    await next_dish(callback)

    
    


@dp.callback_query(lambda query: query.data == 'stop_dish')
async def stop_dish(query:types.CallbackQuery):
    await query.message.answer(text="Вот остальные кнопки",reply_markup = dish_kb.as_markup())

    









async def main():
    await dp.start_polling(bot)


asyncio.run(main())



