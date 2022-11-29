from pydantic import BaseModel, BaseSettings, Field


class Project(BaseModel):
    """
    Описание проекта.
    """

    #: название проекта
    title: str = "References Bot"
    #: описание проекта
    description: str = "Чат-бот для оформления списка использованных источников."
    #: версия релиза
    release_version: str = Field(default="0.1.0")


class ChatBot(BaseModel):
    """
    Конфигурация чат-бота для Telegram.
    """

    #: токен доступа к чат-боту
    api_token: str


class Settings(BaseSettings):
    """
    Настройки проекта.
    """

    #: режим отладки
    debug: bool = Field(default=False)
    #: описание проекта
    project: Project
    #: конфигурация чат-бота для Telegram
    chatbot_telegram: ChatBot
    #: путь к файлу шаблона для заполнения списка литературы
    template_file_path: str = Field(default="/media/template.xlsx")

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


# инициализация настроек приложения
settings = Settings()
