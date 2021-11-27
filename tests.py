from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
import pytest
from unittest.mock import AsyncMock
from main import start_chat, select_payment, select_pizza, keyboard

class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Msg:
    """Тестовые сообщения юнит тестов"""
    def __init__(self, id, username, text) -> None:
        self.from_user = dotdict({
            "username": username,
            "id": id,
        })
        self.chat = dotdict({
            "id": id
        })
        self.text = text
    
    async def reply(self, text: str, reply_markup=0):
        pass
        
test_message_1 = Msg(
    id = 640723148,
    username = "OmicronOne",
    text = "/start"
)

test_message_2 = Msg(
    id = 64075164148,
    username = "MichaelJackson",
    text = "/cancel"
)


@pytest.mark.asyncio
async def test_start_dialog():
    """Тест на создание диалога с пользователем"""
    #В случае успеха функция должна успешно завершиться и вернуть значение 0
    
    response = await start_chat(message=test_message_1)
    assert response == 0
    
@pytest.mark.asyncio
async def test_start_another_dialog():
    """Тест на создание диалога с параллельным пользователем"""
    #В случае успеха функция должна успешно завершиться и вернуть значение 0
    
    response = await start_chat(message=test_message_2)
    assert response == 0
    
@pytest.mark.asyncio
async def test_diaglog_dublicate():
    """Тест на повторное создание диалога без завершения предыдущего"""
    #В случае успеха функция должна завершиться с ошибкой и вернуть значение 1
    
    response = await start_chat(message=test_message_1)
    assert response == 1

@pytest.mark.asyncio
async def test_order_violation():
    """Тест на нарушение порядка стейт-машины"""
    #В случае успеха функция должна завершиться с ошибкой и вернуть значение 1
    
    response = await select_payment(message=test_message_1)
    assert response == 1