from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, Chat
from keyboards.inline import showWeb
from datebase import user
from config import bot_id

router = Router()

@router.message(CommandStart())
async def handle_start_command(message: Message, bot: Bot):

    user_id = message.from_user.id

    if await user.isReg(user_id):
        await message.answer(f"Вітаю в Chroon.\nСуть гри полягає в тому, щоб заробляти монети в різноманітних іграх у вкладці 'Earn' та прокачувати за ці монети своє місто, підвищуючи населення та тип самого міста.\nПід час лістингу кількість населення твого міста буде конвертована в токени, які ти успішно зможеш продати та заробити.\nТакож ти та твої друзі, котрих ти покличеш у гру по реферальному посиланню зможете заробити додаткові бонуси.\nБажаю успіху.", reply_markup=await showWeb())
    else:
        args = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None

        if args and args.startswith('kentId'):
            referrer_id = args[6:]

            if str(user_id) != referrer_id:
                referrer: Chat = await bot.get_chat(int(referrer_id))
                await user.reg_user(user_id, message.from_user.first_name, referrer_id, referrer.first_name)
                
                await message.answer(f"Вітаю в Chroon, ти та твій друг отримуєте по 100.000 монет за перехід по посиланню.\nСуть гри полягає в тому, щоб заробляти монети в різноманітних іграх у вкладці 'Earn' та прокачувати за ці монети своє місто, підвищуючи населення та тип самого міста.\nПід час лістингу кількість населення твого міста буде конвертована в токени, які ти успішно зможеш продати та заробити.\nТакож ти та твої друзі, котрих ти покличеш у гру по реферальному посиланню зможете заробити додаткові бонуси.\nБажаю успіху.", reply_markup=await showWeb())
        else:
            referral_link = f"https://t.me/{bot_id}?start=kentId{user_id}"
            
            await user.reg_user(user_id, message.from_user.first_name)
            
            await message.answer(f"Вітаю в Chroon.\nСуть гри полягає в тому, щоб заробляти монети в різноманітних іграх у вкладці 'Earn' та прокачувати за ці монети своє місто, підвищуючи населення та тип самого міста.\nПід час лістингу кількість населення твого міста буде конвертована в токени, які ти успішно зможеш продати та заробити.\nТакож ти та твої друзі, котрих ти покличеш у гру по реферальному посиланню зможете заробити додаткові бонуси.\nБажаю успіху.", reply_markup=await showWeb())