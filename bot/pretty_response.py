import requests

            
def pretty_dish(response_data):
    for dish in response_data["results"]:
        id = dish["id"]
        dish_text = f"Название: {dish['name']}\n"
        dish_text += f"Кухня: {dish['cuisine']}\n"
        dish_text += f"Тип: {dish['type']}\n"
        dish_text += f"Ингридиенты:\n"
        if dish["ingridients"]:
            for ingr in dish["ingridients"]:
                dish_text += ingr["name"]
        dish_text += f"Время приготовления: {dish['cooking_time']} минут\n"
        if dish['photo']:
            photo = dish['photo']
            dish_text += f'Фото:{photo}\n'


            # dish_text += f"Фото:({dish['photo']})\n"
        dish_text += f"Рецепт: {dish['recipe']}\n"
        dish_text += f"Уровень сложности: {dish['level']}\n"
        dish_text += f"Количество порций: {dish['quant_people']}\n"
        dish_text += f"Описание: {dish['description']}\n"
        dish_text += f"Дата создания: {dish['created_at']}\n"
        dish_text += f"Дата обновления: {dish['updated_at']}\n"
        yield (dish_text, id)

