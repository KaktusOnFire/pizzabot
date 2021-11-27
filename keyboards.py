from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


class PizzaBotKeyboard:
    """Клавиатуры для Telegram бота"""
    
    def __init__(self) -> None:
        self.__pizza_selector_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        self.__payment_selector_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        self.__final_selector_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        self.__empty_kb = ReplyKeyboardRemove()
                
        self.__pizza_selector_kb.add(
            KeyboardButton('🔶Большая'),
            KeyboardButton('🔸Маленькая'),
        )
        
        self.__payment_selector_kb.add(
            KeyboardButton('💳По карте'),
            KeyboardButton('💵Наличкой')
        )
        
        self.__final_selector_kb.add(
            KeyboardButton('✔️Подтверждаю'),
            KeyboardButton('❌Отмена'),
        )
    
    @property
    def pizza_selector_kb(self) -> ReplyKeyboardMarkup:
        return self.__pizza_selector_kb
    
    @property
    def payment_selector_kb(self) -> ReplyKeyboardMarkup:
        return self.__payment_selector_kb
    
    @property
    def final_selector_kb(self) -> ReplyKeyboardMarkup:
        return self.__final_selector_kb
    
    @property
    def empty_kb(self) -> ReplyKeyboardRemove:
        return self.__empty_kb