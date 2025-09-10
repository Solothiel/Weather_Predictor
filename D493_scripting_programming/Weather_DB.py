from sqlalchemy import (Column, Float, Integer)
from sqlalchemy.orm import declarative_base

Base = declarative_base()
#this sets the metadata and column names for the database to be populated.
class WeatherRecord(Base):
    __tablename__ = "weather_data"
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    month = Column(Integer)
    day = Column(Integer)
    year = Column(Integer)
    avg_temp = Column(Float)
    min_temp = Column(Float)
    max_temp = Column(Float)

    avg_wind_speed = Column(Float)
    min_wind_speed = Column(Float)
    max_wind_speed = Column(Float)

    sum_precipitation = Column(Float)
    min_precipitation = Column(Float)
    max_precipitation = Column(Float)


