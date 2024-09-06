from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *

API = ''
BOT = Bot(token=API)
DP = Dispatcher(BOT, storage=MemoryStorage())

get_all_products()

rkb1 = ReplyKeyboardMarkup(resize_keyboard=True)
button1_rkb1 = KeyboardButton(text='Рассчитать калории')
button2_rkb1 = KeyboardButton(text='Информация')
button3_rkb1 = KeyboardButton(text='Купить')
button4_rkb1 = KeyboardButton(text='Регистрация')
rkb1.add(button1_rkb1)
rkb1.add(button2_rkb1)
rkb1.add(button3_rkb1)
rkb1.add(button4_rkb1)

ikb1 = InlineKeyboardMarkup(resize_keyboard=True)
button1_ikb1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2_ikb1 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
ikb1.add(button1_ikb1)
ikb1.add(button2_ikb1)

ikb2 = InlineKeyboardMarkup(resize_keyboard=True)
button1_ikb2 = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
button2_ikb2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
button3_ikb2 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
button4_ikb2 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
ikb2.add(button1_ikb2)
ikb2.add(button2_ikb2)
ikb2.add(button3_ikb2)
ikb2.add(button4_ikb2)


@DP.message_handler(text='Купить')
async def get_buying_list(message):
    for product in get_all_products():
        with open(
                f'C:\\Users\\vavan\\PythonProjectsUrban\\bot_pythonProject\\main_bot_shell\\hmw\\photos\\{product[0]}.png',
                'rb') as img:
            await message.answer_photo(img, f'Название: {product[1]} | {product[2]} | Цена: {product[3]}')
    await message.answer('Выберите продукт для покупки:', reply_markup=ikb2)


@DP.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@DP.message_handler(text='Рассчитать калории')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=ikb1)


@DP.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора:\n- для мужчин:\n  10 х вес (кг) + 6,25 x рост (см) – 5 х '
                              'возраст (г) + 5')
    await call.answer()


@DP.message_handler(commands=['start'])
async def buttons(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью', reply_markup=rkb1)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


@DP.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@DP.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text) is False:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')


@DP.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@DP.message_handler(state=RegistrationState.age)
async def set_email(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer(f'Пользователь успешно зарегистрирован')
    await state.finish()


class UserState(StatesGroup):
    weight = State()
    growth = State()
    age = State()


@DP.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст.')
    await call.answer()
    await UserState.age.set()


@DP.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(user_age=message.text)
    await message.answer('Введите свой рост.')
    await UserState.growth.set()


@DP.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(user_growth=message.text)
    await message.answer('Введите свой вес.')
    await UserState.weight.set()


@DP.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(user_weight=message.text)
    data = await state.get_data()
    result = (10 * int(data['user_weight'])) + (6.25 * int(data['user_growth'])) - ((5 * int(data['user_age'])) + 5)
    await message.answer(f'Ваша норма калорий: {result}')
    await state.finish()


@DP.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(DP, skip_updates=True)
    connection.commit()
    connection.close()
