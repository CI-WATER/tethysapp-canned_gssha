import os
from datetime import datetime, timedelta

from tethys_apps.base.persistent_store import get_persistent_store_engine as gpse


def get_persistent_store_engine(persistent_store_name):
    """
    Returns an SQLAlchemy engine object for the persistent store name provided.
    """
    # Derive app name
    app_name = os.path.split(os.path.dirname(__file__))[1]

    # Get engine
    return gpse(app_name, persistent_store_name)


def decimal_year_to_datetime(decimal_year):
    """
    Convert the decimal year to datetime object
    """

    # Split to year and decimal chunk
    year = int(decimal_year)
    remainder = decimal_year - year

    # Create datetime objects
    base_date = datetime(year, 1, 1)

    full_year_of_seconds = (base_date.replace(year=base_date.year + 1) - base_date).total_seconds()
    remainder_seconds = full_year_of_seconds * remainder
    full_date = base_date + timedelta(seconds=remainder_seconds)

    return full_date