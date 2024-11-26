import os

from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder



def create_button():

    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="G&P", callback_data="G&P черный.png"))
    kb.row(types.InlineKeyboardButton(text="Gordeev&Partners", callback_data="logo_white.png"))

    return kb

def button_after_photo():
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="Выбрать watermark", callback_data="Выбрать watermark"))
    return kb