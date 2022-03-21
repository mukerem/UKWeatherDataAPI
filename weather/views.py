import requests

from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


def get_data(type):
    HEADER_LINES = 5
    url = f"https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{type}/date/UK.txt"
    
    response = requests.get(url)
    data = response.text.strip().split('\n')
    data = data[HEADER_LINES:]
    header = data[0].split()
    year_2022 = data[-1]
    data = data[1:-1]
    result = {}
    keys = header[1:]
    for row in data:
        col = row.split()
        year = col[0]
        values =[]
        for val in col[1:]:
            try:
                values.append(float(val))
            except:
                values.append(None)
        dict_row = dict(zip(keys, values))
        result[year] = dict_row
    year = "2022"
    dict_row = {key: None for key in keys}
    dict_row.update({
        "jan": year_2022[0],
        "feb": year_2022[1],
        "win": year_2022[2]
        })
    result[year] = dict_row
    return result


class WeatherListAPIView(generics.ListAPIView):
    queryset = None

    def get_queryset(self):
        year = self.request.GET.get('year')
        season = self.request.GET.get('season')
        type = self.request.GET.get('type')
        """
        types are:
            1. Tmax
            2. Tmin
            3. Tmean
            4. Sunshine
            5. Rainfall
            6. Raindays1mm
            7. AirFrost
        """
        data = get_data(type) 
        seasonal = data.get(year)
        if seasonal:
            queryset = seasonal.get(season)
            if queryset:
                return Response({"result": queryset})
        return NotFound({"result": f"There is no data for {year} {season}"})


"""
All urls
    url = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmin/date/UK.txt"
    url = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmean/date/UK.txt"
    url = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Sunshine/date/UK.txt"
    url = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Rainfall/date/UK.txt"
    url = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Raindays1mm/date/UK.txt"
    url = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/AirFrost/date/UK.txt"

"""