from telegram import CallbackQuery


class UploadCallbackHandler:
    def handle(self, callback_query: CallbackQuery) -> bool:

        callback_query.edit_message_text(
            text="Пожалуйста, отправьте заполненный файл шаблона со списком литературы.",
        )
        callback_query.answer("Ожидание загрузки файла")

        return True
