from django.db import models


class PopularCity(models.Model):
    """Таблица с названиями популярных городов, которые будут выведены на главной странице."""

    city_name = models.CharField(max_length=255)

    def __str__(self):
        return self.city_name

    class Meta:
        db_table = "popular_city"
        verbose_name = "Популярный город"
        verbose_name_plural = "Популярные города"
