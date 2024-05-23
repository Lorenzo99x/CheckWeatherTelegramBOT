from Weather import WeatherI
from threeb_weather import ThreeBWeather


class WeatherFactory:
    def create_weather_getter(getter_type: str, **kwargs) -> WeatherI:
        if getter_type in "3bmeteo":
            return ThreeBWeather()
        else:
            return None
        # other weather_getter
