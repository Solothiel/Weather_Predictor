from Weather_Class import WeatherData
from Weather_DB import WeatherRecord, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

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
        min_wind_spee=weather_data.five_year_min_wind,
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