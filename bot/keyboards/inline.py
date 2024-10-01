from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

async def showWeb():
    button_play = InlineKeyboardButton(text='Play', web_app=WebAppInfo(url='https://ch1ps.pythonanywhere.com/'))
    button_channel = InlineKeyboardButton(text='Subscribe to the channel', url='https://t.me/hamster_kombat')
    button_help = InlineKeyboardButton(text='How to play', callback_data='help_game')

    webKeyboard = InlineKeyboardMarkup(inline_keyboard=[
        [button_play],
        [button_channel],
        [button_help]
    ])

    return webKeyboard