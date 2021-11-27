import logging
from aiogram import Bot, Dispatcher, executor, types
from keyboards import PizzaBotKeyboard
from machines import PizzaMachine
from aiogram.types import KeyboardButton
from orders import PizzaOrder
import os

API_TOKEN = os.getenv("API_TOKEN")


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
keyboard = PizzaBotKeyboard()
machines = {}
orders = []

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="start")
async def start_chat(message: types.Message):
    try: 
        client = machines[f"{message.chat.id}"]
    except KeyError:
        client = PizzaMachine(f"{message.chat.id}")
        machines[f"{message.chat.id}"] = client
        
    if client.state == "Ожидание":
        client.selecting_pizza()
        await message.reply("Какую пиццу вы хотите?", reply_markup=keyboard.pizza_selector_kb)
        return 0
         
    else:
        await message.reply("Вы не завершили предыдущее действие!")
        return 1
         

@dp.message_handler(commands="cancel")
async def action_cancel(message: types.Message):
    try: 
        client = machines[f"{message.chat.id}"]
    except KeyError:
        await message.reply("Похоже, что вы ещё не заказывали у нас пиццу! Введите /start для оформления заказа", reply_markup=keyboard.empty_kb)
        return 1
         
    
    if client.state != "Ожидание":
        client.cancel()
        client.clear_selections()
        await message.reply("Отмена! Введите /start чтобы попробовать ещё раз.", reply_markup=keyboard.empty_kb)
        return 0
        
    else:
        await message.reply("У вас нет активных заказов! Введите /start для оформления заказа", reply_markup=keyboard.empty_kb)
        return 1
        

@dp.message_handler(lambda message: KeyboardButton(message.text) in keyboard.pizza_selector_kb.keyboard[0])
async def select_pizza(message: types.Message):
    try: 
        client = machines[f"{message.chat.id}"]
    except KeyError:
        await message.reply("Похоже, что вы ещё не заказывали у нас пиццу! Введите /start для оформления заказа", reply_markup=keyboard.empty_kb)
        return 1
        
        
    if client.state == "Выбираем пиццу":
        client.selecting_payment()
        client.selected_pizza = message.text
        await message.reply("Как будем оплачивать?", reply_markup=keyboard.payment_selector_kb)
        return 0
        
    else:
        await message.reply("Вы не завершили предыдущее действие! Нажмите /start чтобы начать заново.")
        return 1
        

@dp.message_handler(lambda message: KeyboardButton(message.text) in keyboard.payment_selector_kb.keyboard[0])
async def select_payment(message: types.Message):
    try: 
        client = machines[f"{message.chat.id}"]
    except KeyError:
        await message.reply("Похоже, что вы ещё не заказывали у нас пиццу! Введите /start для оформления заказа", reply_markup=keyboard.empty_kb)
        return 1
        
    
    if client.state == "Выбираем тип оплаты":
        client.confirmation()
        client.selected_payment = message.text
        await message.reply(
            "Подтвердите ваш выбор:\n"\
            f"Размер пиццы - {client.selected_pizza}\n"\
            f"Тип оплаты - {client.selected_payment}", reply_markup=keyboard.final_selector_kb)
        return 0
        
    else:
        await message.reply("Вы не завершили предыдущее действие! Нажмите /start чтобы начать заново.")
        return 1
        
        
@dp.message_handler(lambda message: KeyboardButton(message.text) in keyboard.final_selector_kb.keyboard[0])
async def confirmation(message: types.Message):
    try: 
        client = machines[f"{message.chat.id}"]
    except KeyError:
        await message.reply("Похоже, что вы ещё не заказывали у нас пиццу! Введите /start для оформления заказа", reply_markup=keyboard.empty_kb)
        return 1
        
    
    if client.state == "Подтверждение":
        client.getting_ready()
        client.clear_selections()
        if message.text == "✔️Подтверждаю":
            client.update_journal()
            orders.append(PizzaOrder(
                client = message.from_user.username,
                pizza = client.selected_pizza,
                payment = client.selected_payment,
                source = "Telegram Pizzabot"
            ))
            
            await message.reply(
                "Спасибо за заказ!\n"\
                f"Количество ваших заказов - {client.pizzas_buyed}\n"\
                "Нажмите /start чтобы сделать новый заказ.", reply_markup=keyboard.empty_kb)
            return 0
            
        else:
            await message.reply("Заказ отменён! Нажмите /start чтобы сделать новый заказ.", reply_markup=keyboard.empty_kb)
            return 2
            
    else:
        await message.reply("Вы не завершили предыдущее действие! Нажмите /start чтобы начать заново.")
        return 1
        
    
@dp.message_handler(lambda message: message.text == "❌Отмена")
async def cancel(message: types.Message):
    try: 
        client = machines[f"{message.chat.id}"]
    except KeyError:
        await message.reply("Похоже, что вы ещё не заказывали у нас пиццу! Введите /start для оформления заказа", reply_markup=keyboard.empty_kb)
        return 1
        
    
    if client.state != "Ожидание":
        client.cancel()
        client.clear_selections()
        await message.reply("Отмена! Введите /start для оформления заказа", reply_markup=keyboard.empty_kb)
        return 0
        
    else:
        await message.reply("У вас нет активных заказов! Введите /start для оформления заказа", reply_markup=keyboard.empty_kb)
        return 1
        



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)