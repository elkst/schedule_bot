from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.main_menu import main_menu


async def start_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "Добро пожаловать! Выберите действие из меню ниже.",
        reply_markup=main_menu
    )
