import requests
from json import loads
from loguru import logger

from .config import MainConfig
from .models import PopularCity


@logger.catch
def get_all_cities_for_popular_city_model() -> list:
    """Возвращает список названий городов из таблицы популярных городов PopularCity"""

    all_cities = PopularCity.objects.all()
    return [city.city_name for city in all_cities]


@logger.catch
def get_weather_for_all_popular_cities() -> list:
    """
    Возвращает список словарей, каждый словарь имеет параметры, отображающие данные о погоде в каждом городе из
    таблицы PopularCity
    """
    all_cities = get_all_cities_for_popular_city_model()
    return [get_weather_info_for_city_from_my_form(city) for city in all_cities]


@logger.catch
def get_weather_info_for_city_from_my_form(city_name: str) -> dict:
    """Возвращает словарь с параметрами, которые буду выводиться в ответе на запрос погоды по конкретному городу"""

    weather_info_for_city = {
        'city_name': city_name,
        'temperature_now': get_temperature_info_for_city_now(city_name, 'temp'),
        'feels_like_now': get_temperature_info_for_city_now(city_name, 'feels_like'),
        'humidity_now': get_temperature_info_for_city_now(city_name, 'humidity'),
        'weather_icon_now': get_weather_info_for_city_now(city_name, 'icon'),
        'weather_description_now': get_weather_info_for_city_now(city_name, 'description'),
        'wind_speed_now': get_wind_speed_for_city_now(city_name),
    }
    return weather_info_for_city


@logger.catch
def get_all_weather_info_for_city_now(city_name: str, api_key=MainConfig.API_KEY) -> dict:
    """
    Отдает словарь со всеми данными о погоде в городе city_name на текущее время.
    Словарь получается десериализацией из json формата, которы мы получаем из api.
    В api передается город city_name и api ключ api_key
    """
    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}&lang=ru'
    all_weather_for_city = requests.get(api_url).text
    return loads(all_weather_for_city)


@logger.catch
def get_temperature_info_for_city_now(city_name: str, temperature_type: str) -> str:
    """
    Отдает данные о температуре на текущий момент, относящиеся к одному из типов temperature_type:
    'temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity', 'sea_level', 'grnd_level'
    """
    weather_for_city_now = get_all_weather_info_for_city_now(city_name)
    return weather_for_city_now['main'][temperature_type]


@logger.catch
def get_weather_info_for_city_now(city_name: str, context: str) -> str:
    """
    Отдает строку, со значением одного из ключей context:
    'icon' - название картинки изображающей текущую погоду,
    'description' - описание текущий погоды короткой фразой
    """
    weather_for_city = get_all_weather_info_for_city_now(city_name)
    return weather_for_city['weather'][0][context]


@logger.catch
def get_wind_speed_for_city_now(city_name: str) -> str:
    """
    Отдает строку, со значением скорости ветра в метрах в секунду в городе city_name
    """
    weather_for_city = get_all_weather_info_for_city_now(city_name)
    return weather_for_city['wind']['speed']


@logger.catch
def get_coords_for_city(city_name: str, api_key=MainConfig.API_KEY) -> dict | None:
    """
    Принимает название города и возвращает словарь с координатами широты и долготы
    Для получения данных использует api в который передает название города city_name и api ключ api_key
    """

    api_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}&lang=ru'
    coords_for_city = requests.get(api_url).text
    coords_for_city, = loads(coords_for_city)
    return {
        'lat': coords_for_city['lat'],
        'lon': coords_for_city['lon']
    } if all([coords_for_city['lat'], coords_for_city['lon']]) else None
