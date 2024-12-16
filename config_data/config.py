from dataclasses import dataclass
from environs import Env


# Конфиг бота
@dataclass
class TgBot:
    token: str


# Конфиг для базы данных
@dataclass
class Database:
    name: str
    echo: bool


# Глобальный конфиг
@dataclass
class Config:
    tg_bot: TgBot
    db: Database


# Получение конфига
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        ),

        db=Database(
            name=env('BD_NAME'),
            echo=env.bool('BD_ECHO', False)
        )
    )
