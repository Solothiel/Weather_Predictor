from Weather_Class import WeatherData
from Weather_DB import WeatherRecord, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from tabulate import tabulate

def save_weather_to_db (weather_data: WeatherData):
    #This method populates the weather data for the location
    engine = create_engine('sqlite:///weather.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    record = WeatherRecord (
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
    """this executes a query on weather_data table then filters the results 
    and returns the first matching row."""
    existing = session.query(WeatherRecord).filter_by(
        latitude=weather_data.loc_latitude,
        longitude=weather_data.loc_longitude,
        month=weather_data.month,
        day=weather_data.day,
        year=weather_data.year
    ).first()

    """This checks to see if the information gathered is in the database and if not it
        will update the database with a commit and then close the commit"""
    if existing:
        print(f"Record already exists for {weather_data.month}/"
            f"{weather_data.day}/{weather_data.year}. Skipping insert."
        )
    else:
        session.add(record)
        session.commit()
        print(f"Saved weather data for {weather_data.year}.")
        session.close()

def display_all_records():
    """This generates the data for the screenshot displaying in a
        formatted manner"""
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

def main():
    """ This is the instance to call methods for the daily weather variables, currently
        I have the information hard coded for Idaho falls June 15 2024"""
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

    """this it the instance that starts the call Weather_Class.py 
     and the WeatherData class."""
if __name__ == "__main__":
    main()