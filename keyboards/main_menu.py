from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    """
    Создает главное меню с кнопками для взаимодействия.
    """
    buttons = [
        [InlineKeyboardButton(text="📅 Расписание", callback_data="schedule")],
        [InlineKeyboardButton(text="👥 Моя группа", callback_data="group")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")],
        [InlineKeyboardButton(text="ℹ️ О боте", callback_data="about")],
        [InlineKeyboardButton(text="🔐 Админка", callback_data="admin")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
