from typing import List, Dict, Optional
from abc import ABC, abstractmethod


class WeatherI(ABC):
    @abstractmethod
    def get_weather():
        # method to get weather
        pass
