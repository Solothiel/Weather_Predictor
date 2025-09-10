from weather_class import WeatherData
from Weather_DB import WeatherRecord, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# This populates the weather data for the location.
def save_weather_to_db(weather_data: WeatherData):
    engine = create_engine('sqlite:///weather.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()


    record = WeatherRecord(
        latitude=weather_data.loc_latitude,
        longitude=weather_data.loc_longitude,
        month=weather_data.month,
        day=weather_data.day,
        year=weather_data.year,

        avg_temp=weather_data.five_year_avg_temp,
        min_temp=weather_data.five_year_min_temp,
        max_temp=weather_data.five_year_max_temp,

        avg_wind_speed=weather_data.five_year_avg_wind,
        min_wind_speed=weather_data.five_year_min_wind,
        max_wind_speed=weather_data.five_year_max_wind,

        sum_precipitation=weather_data.five_year_sum_precip,
        min_precipitation=weather_data.five_year_min_precip,
        max_precipitation=weather_data.five_year_max_precip
    )
    existing = session.query(WeatherRecord).filter_by(
        latitude=weather_data.loc_latitude,
        longitude=weather_data.loc_longitude,
        month=weather_data.month,
        day=weather_data.day,
        year=weather_data.year
    ).first()

    if existing:
        print(f"Record already exists for {weather_data.month}/{weather_data.day}/{weather_data.year}. Skipping insert.")
    else:
        session.add(record)
        session.commit()
        print(f"Saved weather data for {weather_data.year}.")
        session.close()


# this generates the data for the screen shot displaying in a formatted manner.
def display_all_records():
    engine = create_engine('sqlite:///weather.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    records = session.query(WeatherRecord).all()
    for record in records:
        print(f"\nWeather Data for {record.month}/{record.day}/{record.year}")
        print(f"Latitude: {record.latitude}")
        print(f"Longitude: {record.longitude}")
        print(f"Avg Temp: {record.avg_temp} °F")
        print(f"Min Temp: {record.min_temp} °F")
        print(f"Max Temp: {record.max_temp} °F")
        print(f"Avg Wind Speed: {record.avg_wind_speed} mph")
        print(f"Min Wind Speed: {record.min_wind_speed} mph")
        print(f"Max Wind Speed: {record.max_wind_speed} mph")
        print(f"Sum Precipitation: {record.sum_precipitation} in")
        print(f"Min Precipitation: {record.min_precipitation} in")
        print(f"Max Precipitation: {record.max_precipitation} in")

    session.close()
#this is the instance to call the methods for daily weather variables.
def main():
    latitude = 43.4927
    longitude = -112.0408
    month = 6
    day = 15
    year = 2024

    weather = WeatherData(latitude, longitude, month, day, year)
    weather.fetch_temperature_5yr()
    weather.fetch_wind_5yr()
    weather.fetch_precip_5yr()

    save_weather_to_db(weather)
    display_all_records()

# For c3 this it the instance that starts the call weather_class.py and the WeatherData class
if __name__ == "__main__":
    main()
