from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Основное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("📅 Расписание"), KeyboardButton("👥 Мои группы"))
main_menu.add(KeyboardButton("⚙ Настройки"))
