"""Абстрактный базовый класс для работы с внешними API."""

from abc import ABC, abstractmethod
from typing import Optional


class AbstractAPI(ABC):
    """Абстрактный интерфейс для получения данных о самолетах и границах стран.

    Конкретные реализации наследуют этот класс и реализуют все абстрактные методы.
    Это обеспечивает подставляемость разных источников данных без изменения
    использующего их кода (Open-Closed Principle).
    """

    @abstractmethod
    def get_country_bbox(self, country_name: str) -> Optional[list[float]]:
        """Получить координаты границ страны.

        Args:
            country_name: Название страны на английском.

        Returns:
            Список [min_lat, max_lat, min_lon, max_lon] или None при ошибке.
        """
        pass

    @abstractmethod
    def get_aeroplanes_in_bbox(self, min_lat: float, max_lat: float,
                               min_lon: float, max_lon: float) -> list[list]:
        """Получить самолеты внутри прямоугольной области.

        Args:
            min_lat: Минимальная широта.
            max_lat: Максимальная широта.
            min_lon: Минимальная долгота.
            max_lon: Максимальная долгота.

        Returns:
            Список state vectors из OpenSky API.
        """
        pass
