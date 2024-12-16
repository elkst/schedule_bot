from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from database.database import async_session
from database.models import Group, Schedule
from states.user_states import UserStates  # Импортируем состояния

router = Router()


# === Стартовое сообщение === #
@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    """
    Приветствие пользователя и выбор группы.
    """
    # Устанавливаем состояние group_selection
    await state.set_state(UserStates.group_selection)

    # Отправляем сообщение с предложением выбрать группу
    await message.answer(
        "Добро пожаловать! Выберите свою группу, чтобы увидеть расписание.",
        reply_markup=await generate_groups_keyboard()
    )


# === Генерация клавиатуры с группами === #
async def generate_groups_keyboard():
    """
    Генерирует клавиатуру с кнопками доступных групп.
    """
    async with async_session() as session:
        result = await session.execute(select(Group))
        groups = result.scalars().all()

    if not groups:
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Нет доступных групп", callback_data="no_groups")]]
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=group.name, callback_data=f"group_{group.id}")]
            for group in groups
        ]
    )
    return keyboard


# === Обработка выбора группы === #
@router.callback_query(lambda c: c.data.startswith("group_"))
async def select_group(callback_query: CallbackQuery, state: FSMContext):
    """
    Сохраняет выбранную группу пользователя и предлагает посмотреть расписание.
    """
    group_id = int(callback_query.data.split("_")[1])

    async with async_session() as session:
        group = await session.get(Group, group_id)

    if not group:
        await callback_query.message.answer("Выбранная группа не найдена. Попробуйте снова.")
        return

    # Сохраняем группу в состояние
    await state.update_data(selected_group_id=group_id)

    # Переводим пользователя в состояние для просмотра расписания
    await state.set_state(UserStates.viewing_schedule)

    await callback_query.message.answer(
        f"Вы выбрали группу: {group.name}. Теперь вы можете посмотреть расписание.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Показать расписание", callback_data="view_schedule")],
                [InlineKeyboardButton(text="Изменить группу", callback_data="change_group")],


            ]
        )
    )


# === Обработка кнопки "Показать расписание" === #
@router.callback_query(lambda c: c.data == "view_schedule")
async def view_schedule(callback_query: CallbackQuery, state: FSMContext):
    """
    Отображает расписание для выбранной группы.
    """
    user_data = await state.get_data()
    group_id = user_data.get("selected_group_id")

    if not group_id:
        await callback_query.message.answer("Группа не выбрана. Пожалуйста, выберите свою группу.")
        return

    async with async_session() as session:
        result = await session.execute(
            select(Schedule).where(Schedule.group_id == group_id).order_by(Schedule.day, Schedule.time)
        )
        schedules = result.scalars().all()

    if not schedules:
        await callback_query.message.answer("Для выбранной группы расписание отсутствует.")
        return

    schedule_text = "\n".join([f"{schedule.day} {schedule.time} - {schedule.subject}" for schedule in schedules])
    await callback_query.message.answer(f"Расписание:\n{schedule_text}")


# === Обработка кнопки "Изменить группу" === #
@router.callback_query(lambda c: c.data == "change_group")
async def change_group(callback_query: CallbackQuery, state: FSMContext):
    """
    Позволяет пользователю изменить свою группу.
    """
    # Переводим пользователя в состояние выбора новой группы
    await state.set_state(UserStates.group_selection)

    await callback_query.message.answer(
        "Выберите новую группу:",
        reply_markup=await generate_groups_keyboard()
    )


# === Помощь пользователю === #
@router.message(Command("help"))
async def help_command(message: types.Message):
    """
    Выводит информацию о командах бота.
    """
    await message.answer(
        "Доступные команды:\n"
        "/start - Запустить бота\n"
        "/help - Помощь\n"
        "Вы можете выбрать свою группу и посмотреть расписание."
    )


# === Регистрация хэндлеров === #
def register_handlers(dp: Router):
    dp.include_router(router)
