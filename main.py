from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
import asyncio

from database.database import init_db
from dialogs.schedule_dialog import schedule_dialog
from middlewares.auth import AuthMiddleware
from handlers import admin, user
from config import Config


async def set_commands(bot: Bot):
    """
    Устанавливает команды для бота в интерфейсе Telegram.
    """
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/help", description="Получить помощь"),
        BotCommand(command="/admin", description="Панель администратора"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """
    Основная функция для запуска бота.
    """
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрируем middleware
    dp.update.middleware(AuthMiddleware(admin_ids=[Config.ADMIN_ID]))

    # Регистрируем базы данных
    await init_db()

    # Настраиваем aiogram-dialog
    setup_dialogs(dp, schedule_dialog)

    # Регистрируем обработчики
    admin.register_handlers(dp)
    user.register_handlers(dp)

    # Устанавливаем команды
    await set_commands(bot)

    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
