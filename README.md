# 💱 Currency Bot

Телеграм-бот для конвертации валют в молдавские леи (MDL).

## Что умеет:
- Конвертирует USD → MDL
- Конвертирует EUR → MDL
- Показывает актуальный курс при старте
- Использует реальный курс с exchangerate-api.com

## Как запустить:
1. Клонируй репозиторий
2. Создай виртуальное окружение: `python -m venv venv`
3. Активируй: `venv\Scripts\activate`
4. Установи зависимости: `pip install -r requirements.txt`
5. Создай файл `.env` и добавь туда: `BOT_TOKEN=твой_токен`
6. Запусти: `python main.py`

## Стек:
- Python 3.10
- aiogram 3.x
- exchangerate-api.com
