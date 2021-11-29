# PizzaBot - Telegram бот для заказа пиццы!
В качестве стейт-машины используется [transitions] <br>
Ссылка - [AwesomePizzaBot]

[transitions]: https://github.com/pytransitions/transitions
[AwesomePizzaBot]: https://t.me/AwesomePizzaBot

## Установка
```bash
docker build -t pizzabot .
```

## Запуск
```bash
docker run pizzabot
```

## Тестирование
```bash
pytest tests.py
```
