import asyncio

from aiogram import Bot, Dispatcher,types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext


from decouple import config


from kbds import activate_kb,start_kb
from states import *
from send_requests import *


TOKEN = config('BOT_TOKEN')


bot = Bot(TOKEN)

dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message:types.Message):
    await message.answer(text = 'Приветствую тебя в боте Goodzy',reply_markup=start_kb.as_markup())

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
    # await bot.edit_message_reply_markup(chat_id = query.message.chat.id,message_id=query.message.message_id)
    res = await user.login_api()
    if res == False:
        await query.message.answer(text='Братишка, ты еще не активировал',reply_markup=activate_kb.as_markup())
    else:
        await query.message.answer(text="Вы успешно активировали аккаунт, и вошли в систему")
    

    
    
    








async def main():
    await dp.start_polling(bot)


asyncio.run(main())



