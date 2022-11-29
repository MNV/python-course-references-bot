import logging
from io import BytesIO

from telegram import Update

from formatters.styles.gost import GOSTCitationFormatter
from readers.reader import SourcesReader
from renderer import Renderer

logger = logging.getLogger()


class UploadMessageHandler:
    """
    Функцкии для обработки загруженного файла.
    """

    def handle(self, update: Update) -> bool:
        """
        Обработка события загрузки файла.

        :param update: Объект с данными, поступившими от чат-бота.
        :return:
        """

        # получение объекта пользовательского файла
        user_file = update.message.effective_attachment.get_file()
        # считывание файла в память (в виде байтов)
        user_file_content = user_file.download_as_bytearray()
        # формирование моделей объектов
        models = SourcesReader(BytesIO(user_file_content)).read()
        # форматирование моделей
        formatted_models = tuple(
            str(item) for item in GOSTCitationFormatter(models).format()
        )

        logger.info("Генерация выходного файла ...")
        output_file = BytesIO()
        Renderer(formatted_models).render(output_file)
        output_file.seek(0)

        # отправка ответа чат-боту
        update.effective_chat.send_document(
            document=output_file,
            filename="bibliography.docx",
            caption="Список литературы",
            disable_content_type_detection=False,
        )

        logger.info("Команда успешно завершена.")

        return True
