from typing import Any

from telegram import ReplyKeyboardMarkup, Update

from handlers.command.base import CommandHandler


class StartCommandHandler(CommandHandler):
    """
    Обработчик команды `/start`.
    """

    def handle(self, update: Update, **kwargs: Any):
        """
        Начало работы с чат-ботом.

        :param update: Объект с данными, поступившими от чат-бота.
        :return:
        """

        keyboard = ReplyKeyboardMarkup(
            keyboard=kwargs["keyboard"], resize_keyboard=True
        )
        update.effective_chat.send_message(
            text=f"Добро пожаловать, {update.message.chat.first_name}!" + "\n\n"
            "Желаем приятного пользования сервисом.\n\n"
            'Список команд бота раскрывается при вводе символа "/".\n'
            "Также команды доступны в основном кнопочном меню бота.\n\n"
            "/help - руководство пользователя.\n",
            reply_markup=keyboard,
        )
