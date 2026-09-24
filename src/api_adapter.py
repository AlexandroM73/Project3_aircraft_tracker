"""Реализация API-адаптера: Nominatim (геоданные) + OpenSky (самолеты)."""

from typing import Optional

import requests

from abstract_api import AbstractAPI


class APIAdapter(AbstractAPI):
    """Конкретная реализация AbstractAPI.

    Использует Nominatim OpenStreetMap для получения границ стран
    и OpenSky Network для получения данных о самолетах.
    """

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_STATES_URL = "https://opensky-network.org/api/states/all"

    def __init__(self) -> None:
        """Инициализация HTTP-сессии с User-Agent (требование Nominatim)."""
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": "AircraftTrackerProject/1.0"})

    def get_country_bbox(self, country_name: str) -> Optional[list[float]]:
        """Получить координаты границ страны через Nominatim API.

        Args:
            country_name: Название страны на английском.

        Returns:
            Список [min_lat, max_lat, min_lon, max_lon] или None при ошибке.
        """
        try:
            params = {
                "q": country_name,
                "format": "json",
                "addressdetails": 1,
                "limit": 1,
            }
            resp = self._session.get(self.NOMINATIM_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if not data:
                return None

            bbox_str = data[0].get("boundingbox")
            if bbox_str and len(bbox_str) == 4:
                return [float(x) for x in bbox_str]
            return None
        except requests.RequestException as e:
            print(f"Ошибка получения границ для {country_name}: {e}")
            return None
        except (ValueError, KeyError, TypeError) as e:
            print(f"Ошибка обработки данных границ {country_name}: {e}")
            return None

    def get_aeroplanes_in_bbox(self, min_lat: float, max_lat: float,
                               min_lon: float, max_lon: float) -> list[list]:
        """Получить самолеты в заданной прямоугольной области через OpenSky API.

        OpenSky отдает все states, фильтрация по bbox выполняется локально.

        Args:
            min_lat: Минимальная широта.
            max_lat: Максимальная широта.
            min_lon: Минимальная долгота.
            max_lon: Максимальная долгота.

        Returns:
            Список state vectors, попавших в bbox.
        """
        try:
            resp = self._session.get(self.OPENSKY_STATES_URL, timeout=15)
            resp.raise_for_status()
            states = resp.json().get("states", [])

            filtered = []
            for state in states:
                lat = state[6]
                lon = state[5]
                if lat is None or lon is None:
                    continue
                if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                    filtered.append(state)
            return filtered
        except requests.RequestException as e:
            print(f"Ошибка получения данных самолетов: {e}")
            return []
        except (ValueError, KeyError, TypeError) as e:
            print(f"Ошибка обработки данных самолетов: {e}")
            return []
