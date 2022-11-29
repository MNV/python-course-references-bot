"""
Базовые функции форматирования списка источников
"""

import logging

from formatters.styles.base import BaseCitationStyle

logger = logging.getLogger()


class BaseCitationFormatter:
    """
    Базовый класс для итогового форматирования списка источников.
    """

    def __init__(self, formatted_items: list[BaseCitationStyle]) -> None:
        """
        Конструктор.

        :param formatted_items: Список объектов для итогового форматирования
        """

        self.formatted_items = formatted_items

    def format(self) -> list[BaseCitationStyle]:
        """
        Форматирование списка источников.

        :return:
        """

        logger.info("Общее форматирование ...")

        return sorted(self.formatted_items, key=lambda item: item.formatted)
