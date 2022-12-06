"""
Функции взаимодействия с API Telegram.
"""
import logging

from telegram import Bot, ParseMode, ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Filters,
    Handler,
    MessageHandler,
    Updater,
)
from telegram.ext.utils.types import CCT

from handlers.callback.upload import UploadCallbackHandler
from handlers.command.gettemplate import GetTemplateCommandHandler
from handlers.command.start import StartCommandHandler
from handlers.command.upload import UploadCommandHandler
from handlers.message.upload import UploadMessageHandler
from menu.upload import UploadMenu
from settings import settings

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class ChatBotTelegram:
    """
    Чат-бот для Telegram.
    """

    # команды чат-бота
    KEYBOARD_COMMANDS = {
        "📥 Скачать шаблон": "gettemplate",
        "📤 Загрузить список литературы": "upload",
        "ℹ️ Техподдержка": "help",
    }

    def __init__(self, updater_object: Updater):
        """
        Конструктор.

        :param updater_object: Объект для получения обновлений (сообщений пользователя) от чат-бота.
        """

        self.updater = updater_object
        # обработчики команд
        self.start_command_handler = StartCommandHandler()
        self.gettemplate_command_handler = GetTemplateCommandHandler()
        self.upload_command_handler = UploadCommandHandler()

        # обработчики функций обратного вызова
        self.upload_callback_handler = UploadCallbackHandler()

    def add_handler(self, handler: Handler[Update, CCT]) -> None:
        """
        Добавление обработчиков команд от пользователя чат-бота.

        :param handler: Обработчик команд.
        :return:
        """

        self.updater.dispatcher.add_handler(handler)  # type: ignore

    def start(self) -> None:
        """
        Запуск функций взаимодействия с Telegram
        для получения обновлений (сообщений от пользователя) и их обработки.

        :return:
        """

        self.updater.start_polling()
        self.updater.idle()

    def command_start(
        self,
        update: Update,
        context: CallbackContext,  # pylint: disable=unused-argument
    ) -> None:
        """
        Обработка команды `/start`.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        keyboard = [[button] for button in self.KEYBOARD_COMMANDS]
        self.start_command_handler.handle(update, keyboard=keyboard)

    def command_gettemplate(
        self,
        update: Update,
        context: CallbackContext,  # pylint: disable=unused-argument
    ) -> None:
        """
        Обработка команды `/gettemplate`.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        self.gettemplate_command_handler.handle(update)

    def command_upload(
        self,
        update: Update,
        context: CallbackContext,  # pylint: disable=unused-argument
    ) -> None:
        """
        Обработка команды `/upload`.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        self.upload_command_handler.handle(update)

    def command_help(
        self,
        update: Update,
        context: CallbackContext,  # pylint: disable=unused-argument
    ) -> None:
        """
        Обработка команды `/help`.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        update.effective_chat.send_message(  # type: ignore
            text="По вопросам работы сервиса и техподдержки направляйте, пожалуйста, "
            "сообщения пользователю @MichaelNV.\n\n"
            "Будем рады вашим предложениям и пожеланиям!\n\n",
            parse_mode=ParseMode.HTML,
        )

    def cancel(
        self,
        update: Update,
        context: CallbackContext,  # pylint: disable=unused-argument
    ) -> int:
        """
        Завершение взаимодействия с чат-ботом.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        update.message.reply_text(
            "Спасибо, что обратились к нашему сервису.",
            reply_markup=ReplyKeyboardRemove(),
        )

        return ConversationHandler.END

    @staticmethod
    def message_unknown(
        update: Update, context: CallbackContext  # pylint: disable=unused-argument
    ) -> None:
        """
        Обработка неизвестного чат-боту текстового сообщения.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        update.effective_chat.send_message(  # type: ignore
            text="Пока не очень понимаю что имелось в виду.\n\n"
            'Список доступных команд раскрывается при вводе символа "/".\n'
            "Техподдержка – /help.\n",
        )

    def callback_handler(
        self,
        update: Update,
        context: CallbackContext,  # pylint: disable=unused-argument
    ) -> str:
        """
        Обработка функций обратного вызова.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        UploadCallbackHandler().handle(update.callback_query)

        return update.callback_query.data

    def text_message_handler(self, update: Update, context: CallbackContext) -> None:
        """
        Обработка текстовых сообщений от пользователя.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        # поиск команды и её выполнение
        if command_name := self.KEYBOARD_COMMANDS.get(update.message.text):
            if method := getattr(self, "command_" + command_name):
                return method(update, context)

            return None

        # обработка неизвестной команды
        return self.message_unknown(update, context)

    def citation_gost(
        self,
        update: Update,
        context: CallbackContext,  # pylint: disable=unused-argument
    ) -> None:
        """
        Обработка поступающих файлов от пользователя.
        Форматирование списка литературы по ГОСТ Р 7.0.5-2008.

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """

        UploadMessageHandler().handle(update)

    def citation_mla(self, update: Update, context: CallbackContext) -> None:
        """
        Обработка поступающих файлов от пользователя.
        Форматирование списка литературы по Modern Language Association.

        todo: реализовать данный метод

        :param update: Объект с данными, поступившими от чат-бота.
        :param context: Объект с данными контекста запроса.
        :return:
        """


try:
    updater = Updater(bot=Bot(settings.chatbot_telegram.api_token))
    bot = ChatBotTelegram(updater)

    # обработка команд
    bot.add_handler(CommandHandler("start", bot.command_start))
    bot.add_handler(CommandHandler("gettemplate", bot.command_gettemplate))
    bot.add_handler(CommandHandler("upload", bot.command_upload))
    bot.add_handler(CommandHandler("help", bot.command_help))

    # обработка команды для загрузки файла
    bot.add_handler(
        ConversationHandler(
            # обработка функций обратного вызова
            entry_points=[
                CallbackQueryHandler(bot.callback_handler, pattern="citation")
            ],
            states={
                UploadMenu.BUTTON_CITATION_GOST: [
                    # обработка сообщения, содержащего документ (файл)
                    MessageHandler(Filters.document, bot.citation_gost),
                ],
                UploadMenu.BUTTON_CITATION_MLA: [
                    # обработка сообщения, содержащего документ (файл)
                    MessageHandler(Filters.document, bot.citation_mla),
                ],
            },
            fallbacks=[CommandHandler("cancel", bot.cancel)],
        )
    )

    # обработка функций обратного вызова
    bot.add_handler(CallbackQueryHandler(bot.callback_handler))
    # обработка текстовых сообщений (кнопочного меню или любого текста)
    bot.add_handler(MessageHandler(Filters.text, bot.text_message_handler))
    # запуск взаимодействия с чат-ботом
    bot.start()

except Exception as exception:
    # todo: реализовать обработку исключений
    raise exception
