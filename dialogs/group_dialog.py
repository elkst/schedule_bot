from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.group_menu import group_menu


async def group_menu_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "Выберите действие для управления группами.",
        reply_markup=group_menu
    )
