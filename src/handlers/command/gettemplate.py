from typing import Any

from telegram import Update

from handlers.command.base import CommandHandler
from settings import settings


class GetTemplateCommandHandler(CommandHandler):
    """
    Обработчик команды `/gettemplate`.
    """

    def handle(self, update: Update, **kwargs: Any) -> None:
        """
        Скачать шаблон для заполнения списка литературы.

        :param update: Объект с данными, поступившими от чат-бота.
        :return:
        """

        if update.effective_chat:
            with open(settings.template_file_path, mode="rb") as file:
                update.effective_chat.send_document(document=file)
