import json

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from db_map import select_shina, create_data_shina

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

import re

from find_request_shina import find_shina

router = Router()


class TypeShina(StatesGroup):
    data_shina = State()
    season_shina = State()


# Команда старт
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"⚠ Для поиска шин по типоразмеру нажмите или введите /searchtyre.")


@router.message(Command("searchtyre"))
async def get_data_shina(message: Message, state: FSMContext):
    await message.answer(
        "Для поиска шин по типоразмеру просто напишите необходимый размер в формате 205 55 16 или 205/55 R16 или 205-55-16")
    await state.set_state(TypeShina.data_shina)


@router.message(TypeShina.data_shina)
async def get_data_shina(message: Message, state: FSMContext):
    if re.fullmatch(r'\d\d\d \d\d \d\d', message.text) or re.fullmatch(r'\d\d\d/\d\d R\d\d', message.text) \
            or re.fullmatch(r'\d\d\d-\d\d-\d\d', message.text):
        if re.fullmatch(r'\d\d\d \d\d \d\d', message.text):
            result = message.text.split(' ')
        elif re.fullmatch(r'\d\d\d/\d\d R\d\d', message.text):
            result = [message.text[0:3], message.text[4:6], message.text[8:10]]
        elif re.fullmatch(r'\d\d\d-\d\d-\d\d', message.text):
            result = message.text.split('-')

        create_data_shina(message.from_user.id, json.dumps(result))

        # Создание клавиатуры
        kb = InlineKeyboardBuilder()
        kb.row(types.InlineKeyboardButton(text="Летние", callback_data="Летн"))
        kb.row(types.InlineKeyboardButton(text="Зимние", callback_data="Зимн"))
        kb.row(types.InlineKeyboardButton(text="Всесезонные", callback_data="Всесезонн")).adjust(3)

        # Внести результат в базу данных
        await message.answer(f'Выберите сезон для типоразмера {message.text}', reply_markup=kb.as_markup())
        await state.set_state(TypeShina.season_shina)

    else:
        await message.answer('Неправильный формат размера шины')
        await message.answer(
            "Для поиска шин по типоразмеру просто напишите необходимый размер в формате 205 55 16 или 205/55 R16 или 205-55-16")
        await state.set_state(TypeShina.data_shina)


@router.callback_query(TypeShina.season_shina)
async def get_season_shina(callback: types.CallbackQuery, state: FSMContext):
    data_shina = select_shina(callback.from_user.id)
    data_shina = json.loads(*data_shina)

    list_shins = find_shina(*data_shina, callback.data)
    for i in list_shins:
        await callback.message.answer(i)
    if list_shins[0] != "Таких шин нет в наличии. Попробуйте ввести другой размер.":
        await callback.message.answer(
            'Для заказа скопируйте нужное название шины и отправьте нашему менеджеру https://t.me/dronovirk\n\nДля нового поиска шины введите или нажмите /searchtyre')
    else:
        await callback.message.answer(
            "Для поиска шин по типоразмеру просто напишите необходимый размер в формате 205 55 16 или 205/55 R16 или 205-55-16")
        await state.set_state(TypeShina.data_shina)


# Команда на случай любого сообщения
@router.message()
async def other_command(message: Message):
    await message.answer("Для поиска шины введите или нажмите /searchtyre")
