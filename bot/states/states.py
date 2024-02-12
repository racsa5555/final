from aiogram.fsm.state import State, StatesGroup

class UserRegisterState(StatesGroup):
    email = State()
    password = State()
    first_name = State()
    last_name = State()
    user = None
    login = State()
