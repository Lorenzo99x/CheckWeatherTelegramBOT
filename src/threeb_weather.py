import requests
import bs4
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from Weather import WeatherI


class ThreeBWeather(WeatherI):
    def __init__(self) -> None:
        pass

    def get_weather(self, city: str, day: str) -> Optional[Dict[str, str]]:
        url = f"https://www.3bmeteo.com/meteo/{city}"
        response = requests.get(url)
        if response.status_code != 200:
            return -1

        soup = BeautifulSoup(response.content, 'html.parser')

        weather = {'city': city, 'day': day}

        info = soup.find('a', title=day, href=f'/meteo/{city}/1')
        if info:
            children_tags = (child for child in info.children if isinstance(
                child, bs4.element.Tag))
            for child in children_tags or []:
                if child.has_attr('alt'):
                    weather['info'] = child['alt']
                    continue
                temperatures = self.find_temperatures(child)
                for temp in temperatures or []:
                    self.set_minmax_temperature(weather, temp)
        return weather

    def set_minmax_temperature(self, weather: Dict[str, int], temp: int) -> None:
        if not temp:
            return
        if 'temp1' not in weather:
            weather['temp1'] = temp
        elif weather['temp1'] > temp:
            weather['temp1'], temp = temp, weather['temp1']
            weather['temp2'] = temp
        else:
            weather['temp2'] = temp

    def find_temperatures(self, line: bs4.element.Tag) -> List[str]:
        temperatures = []
        spans = line.find_all('span', class_='switchcelsius switch-te active')
        for span in spans or []:
            temperatures.append(span.get_text(strip=True))
        return temperatures
