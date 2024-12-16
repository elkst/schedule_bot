from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Меню групп
group_menu = ReplyKeyboardMarkup(resize_keyboard=True)
group_menu.add(KeyboardButton("➕ Добавить группу"), KeyboardButton("📋 Список групп"))
group_menu.add(KeyboardButton("⬅ Назад"))
