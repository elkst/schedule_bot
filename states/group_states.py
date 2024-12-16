from aiogram.fsm.state import StatesGroup, State


class GroupStates(StatesGroup):
    CHOOSING_GROUP_ACTION = State()  # Выбор действия с группами
    ADDING_GROUP = State()  # Добавление новой группы
    REMOVING_GROUP = State()  # Удаление группы
