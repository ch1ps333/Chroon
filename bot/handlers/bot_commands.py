from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def cmdStart(message: Message):
    try:
        if not await isReg(message.from_user.id):
            await state.set_state(Form.lang)
            await message.answer("Hello, choose a language.", reply_markup=displaySelectLanguageMenu())
        else:
            await message.answer(ts("Ви вже зареєстровані.", await getLang(message.from_user.id)))
    except Exception as err:
            print(err)
