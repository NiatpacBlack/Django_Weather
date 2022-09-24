from django import forms


class CityForm(forms.Form):
    """Форма для ввода названия города на главной странице."""

    city_name = forms.CharField(label="", max_length=255)
    city_name.widget.attrs.update(
        {"class": "py-3 form-control", "placeholder": "Введите город"}
    )
