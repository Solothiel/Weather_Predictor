import unittest
from Weather_Class import WeatherData

class TestWeather(unittest.TestCase):

    def setUp(self):
        self.weather = WeatherData(
            loc_latitude=43.49,
            loc_longitude=-112.04,
            month=6,
            day=15,
            year=2024
        )

    def test_fetch_temperature_5yr_real(self):
        self.weather.fetch_temperature_5yr()
        self.assertIsNotNone(self.weather.five_year_avg_temp)
        self.assertIsInstance(self.weather.five_year_avg_temp, (float, int))

    def test_fetch_wind_5yr_real(self):
        self.weather.fetch_wind_5yr()
        self.assertIsNotNone(self.weather.five_year_avg_wind)
        self.assertIsInstance(self.weather.five_year_avg_wind, (float, int))

    def test_fetch_precip_5yr_real(self):
        self.weather.fetch_precip_5yr()
        self.assertIsNotNone(self.weather.five_year_sum_precip)
        self.assertIsInstance(self.weather.five_year_sum_precip, (float, int))


if __name__ == "__main__":
    unittest.main()