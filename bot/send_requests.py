import aiohttp
import logging
import asyncio
API = 'http://34.16.110.19/api/'

class User:
    
    def __init__(self,data):
       self.data = data
       self.headers = {}

    async def register_api(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(url = API + 'user/register/',json = self.data) as response:
                result = await response.json()
                if "email" in result and result["email"] == ["user with this email already exists."]:
                    return f'Пользователь с таким email уже существует'
                return f'Поздрваляю,вы создали аккаунт\nВам на почту пришла ссылка, перейдите по ней, чтобы активировать аккаунт'

    
    async def login_api(self):
        data = self.data.copy()
        data.pop('first_name')
        data.pop('last_name')
        async with aiohttp.ClientSession() as session:
            async with session.post(url = API + 'user/login/',json = data) as response:
                result = await response.json()
                if result.get('detail') == 'No active account found with the given credentials':
                    return False
                else:
                    return True

                # token = result.get('access')
                # self.headers["Authorization"] = f"Bearer {token}"
                # return self.headers



