class PizzaOrder:
    """Оформленные заказы"""
    
    def __init__(self, client: str, pizza: str, payment: str, source: str) -> None:
        self.__client = client
        self.__pizza_size = pizza
        self.__payment_type = payment
        self.__source = source
        
    @property
    def client(self):
        return self.__client
    
    @property
    def pizza_size(self):
        return self.__pizza_size
    
    @property
    def payment_type(self):
        return self.__payment_type
    
    @property
    def source(self):
        return self.__source