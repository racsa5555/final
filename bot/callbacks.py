from aiogram.filters.callback_data import CallbackData

class RatingCallback(CallbackData, prefix = 'rating'):
    rating: int
    dish: int
    action: str