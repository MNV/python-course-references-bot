from typing import Dict, Optional

from telegram import InlineKeyboardButton

from menu.base import BaseMenu


class UploadMenu(BaseMenu):
    """
    Функции меню для загрузки файла.
    """

    # значение кнопки для обозначения цитирования по стандарту ГОСТ Р 7.0.5-2008
    BUTTON_CITATION_GOST = "citation.gost"
    # значение кнопки для обозначения цитирования по стандарту Modern Language Association
    BUTTON_CITATION_MLA = "citation.mla"

    @classmethod
    def get_extra_buttons(cls) -> Optional[Dict[str, str]]:
        """
        Получение дополнительных кнопок для меню.

        :return:
        """

        return {
            "ГОСТ Р 7.0.5-2008": cls.BUTTON_CITATION_GOST,
            "Modern Language Association": cls.BUTTON_CITATION_MLA,
        }

    def build_menu(
        self, buttons: list[InlineKeyboardButton], cols_count: int
    ) -> list[list[InlineKeyboardButton]]:
        """
        Формирование меню на основе переданной конфигурации.

        :param buttons: Список объектов кнопок.
        :param cols_count: Количество колонок.
        :return:
        """

        menu = super().build_menu(buttons, cols_count)
        if len(buttons) == 2:
            menu = super().build_menu(buttons, 1)

        if len(buttons) > 3:
            menu = [
                buttons[:1],
                buttons[1 : len(buttons) - 1],  # noqa: E203
                buttons[-1:],
            ]

        return menu
