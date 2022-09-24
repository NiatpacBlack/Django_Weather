import os

from django_weather.settings import API_KEY


class ApiConfig(object):
    """Апи ключ задается либо в переменной окружения либо непосредственно из файла settings"""

    API_KEY = os.environ.get('API_KEY') or API_KEY
