from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group, Select, Cancel
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.manager.manager import DialogManager
from aiogram.types import CallbackQuery
from states.user_states import UserStates
from database import async_session
from database import Group, Schedule
from sqlalchemy.future import select


async def get_groups(**kwargs):
    """
    Получить список всех групп из базы данных.
    """
    async with async_session() as session:
        result = await session.execute(select(Group))
        groups = result.scalars().all()
    return {"groups": groups}


async def get_schedule(dialog_manager: DialogManager, **kwargs):
    """
    Получить расписание для выбранной группы.
    """
    selected_group_id = dialog_manager.current_context().dialog_data.get("selected_group_id")
    if selected_group_id is None:
        return {"schedule": "Выберите группу для просмотра расписания."}

    async with async_session() as session:
        result = await session.execute(
            select(Schedule).where(Schedule.group_id == selected_group_id)
        )
        schedules = result.scalars().all()

    if not schedules:
        return {"schedule": "Для этой группы расписание отсутствует."}

    schedule_text = "\n".join(
        [f"{item.day}, {item.time}: {item.subject}" for item in schedules]
    )
    return {"schedule": schedule_text}


async def on_group_selected(callback_query: CallbackQuery, widget, manager: DialogManager, item_id: str):
    """
    Обработчик выбора группы.
    """
    manager.current_context().dialog_data["selected_group_id"] = int(item_id)
    await manager.dialog().switch_to(UserStates.viewing_schedule)


schedule_dialog = Dialog(
    Window(
        Const("Выберите группу для просмотра расписания:"),
        Select(
            Format("{item.name}"),
            id="group_select",
            item_id_getter=lambda item: str(item.id),
            items="groups",
            on_click=on_group_selected,
        ),
        Cancel(Const("Отмена")),
        state=UserStates.selecting_group,
        getter=get_groups,
    ),
    Window(
        Format("Расписание для выбранной группы:\n\n{schedule}"),
        Button(Const("Назад"), id="back", on_click=lambda c, w, m: m.dialog().switch_to(UserStates.selecting_group)),
        Cancel(Const("Отмена")),
        state=UserStates.viewing_schedule,
        getter=get_schedule,
    ),
)
