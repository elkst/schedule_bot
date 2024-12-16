from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    CHOOSING_ACTION = State()  # Пользователь выбирает действие
    ENTERING_SCHEDULE = State()  # Пользователь вводит расписание
    EDITING_SETTINGS = State()  # Редактирование настроек
