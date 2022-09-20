from django.shortcuts import render

from .forms import CityForm
from .services import *


@logger.catch
def home_page_view(request):
    form = CityForm()
    city_name = 'Минск'
    if request.method == 'POST':
        if request.POST['city_name']:
            city_name = str(request.POST['city_name'])
    return render(request, 'main/home_page.html', {
        'form': form,
        'weather_info_for_city_from_form': get_weather_info_for_city_from_my_form(city_name),
        'weather_for_all_popular_cities': get_weather_for_all_popular_cities()
    })


@logger.catch
def about_us_page_view(request):
    return render(request, 'main/about_us_page.html')
