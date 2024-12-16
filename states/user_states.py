from aiogram.fsm.state import StatesGroup, State

class UserStates(StatesGroup):
    """
    Класс состояний для пользователя.
    Содержит все состояния, связанные с действиями пользователя в боте.
    """
    # Состояние выбора группы
    selecting_group = State()  # Добавляем это состояние

    # Состояние просмотра расписания
    viewing_schedule = State()

    # Состояние добавления новой группы администратором
    adding_group = State()

    # Состояние редактирования расписания (если потребуется)
    editing_schedule = State()

    # Состояние выбора действия в меню (например, "Моя группа", "Расписание", и т.д.)
    main_menu = State()

    # Состояние в админ панели
    admin_panel = State()

    group_selection = State()