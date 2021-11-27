from transitions import Machine
import re

def remove_emoji(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F" 
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF" 
        u"\U0001F1E0-\U0001F1FF"
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

class PizzaMachine(object):
    """Стейт-машина для заказа пиццы"""
    
    states = [
        'Ожидание', 
        'Выбираем пиццу', 
        'Выбираем тип оплаты', 
        'Подтверждение'
    ]

    def __init__(self, user: str):
        
        self.__user = user
        self.__pizzas_buyed = 0
        self.__selected_pizza = None
        self.__selected_payment = None
        self.machine = Machine(model=self, states=self.states, initial='Ожидание')
        
        self.machine.add_transition(trigger='selecting_pizza', source='Ожидание', dest='Выбираем пиццу')
        self.machine.add_transition(trigger='selecting_payment', source='Выбираем пиццу', dest='Выбираем тип оплаты')
        self.machine.add_transition(trigger='confirmation', source='Выбираем тип оплаты', dest='Подтверждение')
        self.machine.add_transition(trigger='getting_ready', source='Подтверждение', dest='Ожидание')
        
        self.machine.add_transition(trigger='cancel', source='Выбираем пиццу', dest='Ожидание')
        self.machine.add_transition(trigger='cancel', source='Выбираем тип оплаты', dest='Ожидание')
        self.machine.add_transition(trigger='cancel', source='Подтверждение', dest='Ожидание')

    @property
    def user(self):
        return self.__user

    @property
    def pizzas_buyed(self):
        return self.__pizzas_buyed
    
    @property
    def selected_pizza(self):
        return self.__selected_pizza
    
    @property
    def selected_payment(self):
        return self.__selected_payment
    
    @selected_pizza.setter
    def selected_pizza(self, pizza):
        self.__selected_pizza = remove_emoji(pizza)
        
    @selected_payment.setter
    def selected_payment(self, payment):
        self.__selected_payment = remove_emoji(payment)
    
    def update_journal(self):
        self.__pizzas_buyed += 1
        
    def clear_selections(self):
        self.__selected_pizza = None
        self.__selected_payment = None