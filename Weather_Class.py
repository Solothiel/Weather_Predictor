import requests

class WeatherData:
    """this is instance variable for the chosen date and location
    params
        loc_latitude: Float location latitude
        loc_longitude: Float location longitude
        month: INT month of the year represented in MM format
        day: INT day of the month represented in DD format
        year: INT year represented in YYYY format
    """
    def __init__(self, loc_latitude, loc_longitude, month, day, year):
        self.loc_latitude = loc_latitude
        self.loc_longitude = loc_longitude
        self.month = month
        self.day = day
        self.year = year

        """ This is the aggregated stats for the temp, wind speed and precipitation
            by default they are set to None because the data hasn't been gathered yet.
            """
        self.five_year_avg_temp = None
        self.five_year_min_temp = None
        self.five_year_max_temp = None

        self.five_year_avg_wind = None
        self.five_year_min_wind = None
        self.five_year_max_wind = None

        self.five_year_sum_precip = None
        self.five_year_min_precip = None
        self.five_year_max_precip = None

    def fetch_temperature_5yr(self):
        """this is the method for gathering the temperature states and have it
            iterate over the five-year window.
            """
        temps = []
        for year in range(self.year - 4, self.year + 1):
            temp = self.fetch_weather_single_day(year, variable='temperature_2m_mean')
            if temp is not None:
                temps.append(temp)
        if temps:
            self.five_year_avg_temp = sum(temps) / len(temps)
            self.five_year_min_temp = min(temps)
            self.five_year_max_temp = max(temps)
        else:
            print("Temperature data missing.")