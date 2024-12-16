from aiogram.types import Update
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from config import Config


class AuthMiddleware(BaseMiddleware):
    def __init__(self, admin_ids=None):
        self.admin_ids = admin_ids or [Config.ADMIN_ID]
        super().__init__()

    async def __call__(self, handler, event: Update, data: dict):
        # Проверяем, что обновление связано с пользователем
        user_id = None
        if hasattr(event, "message") and event.message:
            user_id = event.message.from_user.id
        elif hasattr(event, "callback_query") and event.callback_query:
            user_id = event.callback_query.from_user.id
        elif hasattr(event, "inline_query") and event.inline_query:
            user_id = event.inline_query.from_user.id

        # Если user_id найден, проверяем права
        if user_id:
            data["is_admin"] = user_id in self.admin_ids
        else:
            data["is_admin"] = False

        return await handler(event, data)
