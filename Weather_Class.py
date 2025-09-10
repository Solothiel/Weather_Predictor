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
        """this is the method for gathering the temperature stats and have it
            iterate over the five-year window. The is also creates the temps list
            adds the data to it.
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

    def fetch_wind_5yr(self):
        """this is the method for gathering the wind stats and have it
            iterate over the five-year window and update the wind list
            and add the data gathered to it."""
        winds = []
        for yr in range(self.year - 4, self.year + 1):
            wind = self.fetch_weather_single_day(yr, variable='windspeed_10m_max')
            if wind is not None:
                winds.append(wind)

        if winds:
            self.five_year_avg_wind = sum(winds) / len(winds)
            self.five_year_min_wind = min(winds)
            self.five_year_max_wind = max(winds)
        else:
            print("Wind data missing.")

    def fetch_precip_5yr(self):
        """this is the method for gathering the precipitation stats and have it
                    iterate over the five-year window and update the precs list
                    and add the data gathered to it."""
        precs = []
        for yr in range(self.year - 4, self.year + 1):
            precip = self.fetch_weather_single_day(yr, variable='precipitation_sum')
            if precip is not None:
                precs.append(precip)

        if precs:
            self.five_year_sum_precip = sum(precs)
            self.five_year_min_precip = min(precs)
            self.five_year_max_precip = max(precs)
        else:
            print("Precipitation data missing.")

    def fetch_weather_single_day(self, year, variable):
        """ This creates the single day variable that is used in the api.
            This is method is used to help generate information on the other methods
            with the class.
            """
        date_str = f"{year}-{self.month:02d}-{self.day:02d}"
        latitude_str = f"{self.loc_latitude:.2f}"
        longitude_str = f"{self.loc_longitude:.2f}"

        url = (
            f"https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={latitude_str}&longitude={longitude_str}"
            f"&start_date={date_str}&end_date={date_str}"
            f"&daily={variable}"
            f"&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch"
            f"&timezone=auto"
        )
        #This is the query responses and it deciphers the error codes that occur.
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            daily = json_data.get("daily", {})
            values = daily.get(variable, [])
            if values:
                return values[0]
            else:
                return None
        elif response.status_code == 404:
            print(f"Error 404: Data not found for {date_str}.")
        elif response.status_code == 500:
            print(f"Error 500: Server error for {date_str}. Try again later.")
        else:
            print(f"Error {response.status_code}: An unknown error occurred for {date_str}.")
        return None