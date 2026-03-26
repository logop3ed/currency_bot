import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message , InlineKeyboardMarkup, InlineKeyboardButton , CallbackQuery

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# Создаём состояния
class ConvertState(StatesGroup):
    waiting_usd = State()
    waiting_eur = State()


# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем объекты инлайн-кнопок
button_1 = InlineKeyboardButton(
    text="💵 USD → MDL", callback_data="usd_click"
)
button_2 = InlineKeyboardButton(
    text="💶 EUR → MDL", callback_data="eur_click"
)

# Создаем объект инлайн-клавиатуры
keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])

# наверху рядом с button_1 и button_2
repeat_button = InlineKeyboardButton(
    text='🔄 Конвертировать ещё',
    callback_data='repeat'
)
keyboard_repeat = InlineKeyboardMarkup(inline_keyboard=[[repeat_button]])


CURS_D = 17
CURS_E = 18


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer('Привет!\nЯ бот курса валют!\nОтправь мне команду /curs и я отправлю тебе нынешний курс')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши /curs чтобы получить курс валют \n '
        'Или напиши /start чтобы попасть в главное меню'
    )

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='curs'))
async def process_curs_command(message: Message):
    await message.answer(
        text='Выберите что конвертируем' , reply_markup=keyboard
    )

@dp.callback_query(F.data == 'usd_click')
async def process_usd_click(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Введите сумму в долларах:')
    await state.set_state(ConvertState.waiting_usd)  # запоминаем что ждём USD

# Когда пользователь написал число — берём его и считаем
@dp.message(ConvertState.waiting_usd)
async def process_usd_amount(message: Message, state: FSMContext):
    amount = float(message.text)
    result = amount * CURS_D
    await message.answer(text=f'{amount} USD = {result} MDL', reply_markup=keyboard_repeat)
    await state.clear()  # сбрасываем состояние

@dp.callback_query(F.data == 'eur_click')
async def process_eur_click(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Введите сумму в евро:')
    await state.set_state(ConvertState.waiting_eur)  # запоминаем что ждём USD

# Когда пользователь написал число — берём его и считаем
@dp.message(ConvertState.waiting_eur)
async def process_eur_amount(message: Message, state: FSMContext):
    amount = float(message.text)
    result = amount * CURS_E
    await message.answer(text=f'{amount} EUR = {result} MDL', reply_markup=keyboard_repeat)
    await state.clear()  # сбрасываем состояние

@dp.callback_query(F.data == 'repeat')
async def process_repeat(callback: CallbackQuery):
    await callback.message.answer(
        text='Выберите что конвертируем',
        reply_markup=keyboard
    )


# Этот хэндлер будет срабатывать на любые ваши сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def no_comand(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Не понимаю что вы хотите '
                 'используйте /help'
        )


if __name__ == '__main__':
    dp.run_polling(bot)