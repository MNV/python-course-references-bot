from typing import Any

from telegram import Update

from handlers.command.base import CommandHandler
from menu.upload import UploadMenu


class UploadCommandHandler(CommandHandler):
    """
    Обработчик команды `/upload`.
    """

    def handle(self, update: Update, **kwargs: Any):
        """
        Загрузить файл со списком литературы для обработки.

        :param update: Объект с данными, поступившими от чат-бота.
        :return:
        """

        menu = UploadMenu()
        extra_buttons = menu.get_extra_buttons()
        reply_markup = menu.set_buttons(extra_buttons).get_menu()

        update.effective_chat.send_message(
            text="Выберите стандарт цитирования:", reply_markup=reply_markup
        )
