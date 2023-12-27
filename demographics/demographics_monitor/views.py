from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import DemographicStatistics, Indicators, Territories
from .forms import UserForms


def index(request):
    if request.method == "POST":
        form = UserForms(request.POST)
        if form.is_valid():
            selected_year = int(form.cleaned_data['year'])
            years = [selected_year - 2, selected_year - 1, selected_year]
    else:
        form = UserForms()
        years = [2020, 2021, 2022]

    indicators = [1, 2, 3, 4, 5, 6]

    data_last_three_years = DemographicStatistics.objects.filter(
        indicator_id__in=indicators,
        territory_id=1,
        year__in=years
    ).order_by('indicator_id')
    data_by_indicator = {}
    for data in data_last_three_years:
        indicator_name = data.indicator.indicator_name
        unit_name = data.indicator.unit_measurement.unit_name
        if indicator_name not in data_by_indicator:
            data_by_indicator[indicator_name] = {'unit': unit_name, 'values': {year: '' for year in years}}
        data_by_indicator[indicator_name]['values'][data.year] = data.value

    values1 = []
    values2 = []
    for y in years:
        values1.append(int(data_by_indicator['Число браков в городской местности']['values'][y]))
        values2.append(int(data_by_indicator['Число браков в сельской местности']['values'][y]))

    context_data = {
        'form': form,
        'data_by_indicator': data_by_indicator,
        'years': years,
        'values1': values1,
        'values2': values2,
    }
    return render(request, "demographics_monitor/index.html", context=context_data)


def about(request):
    """
    Отображает страницу "О сайте".
    Parameters
    ----------
    request : HttpRequest
        Входящий HTTP-запрос.
    Returns
    -------
    HttpResponse
        HTTP-ответ, который возвращает HTML-страницу "О сайте".
    """
    return render(request, 'demographics_monitor/about.html')
