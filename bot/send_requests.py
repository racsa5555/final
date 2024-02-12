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
        if 'first_name' in data and 'last_name' in data:
            data.pop('first_name')
            data.pop('last_name')
        async with aiohttp.ClientSession() as session:
            async with session.post(url = API + 'user/login/',json = data) as response:
                result = await response.json()
                if result.get('detail') == 'No active account found with the given credentials':
                    return False
                else:
                    self.headers = {'Authorization': 'Bearer ' + result.get('access')}
                    return True

    async def get_dishes(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url = API + 'dish/') as response:
                result = await response.json()
                return result
    
    async def rating(self,dish_id,rating):
        data = {'rating':rating}
        async with aiohttp.ClientSession() as session:
            async with session.post(url = API + f'dish/{dish_id}/rating/',json = data,headers = self.headers) as response:
                return await response.text()




