
import pandas as pd


def find_less_crowded_hours(data):

    # Check whether data is available
    if data.empty:
        return None

    # Work on a copy of the data
    data = data.copy()

    # Convert timestamps into datetime format
    data["observed_at"] = pd.to_datetime(data["observed_at"])

    # Extract the hour from each timestamp
    data["hour"] = data["observed_at"].dt.hour

    # Calculate average occupancy for each hour
    average_occupancy = data.groupby("hour")["occupancy"].mean()

    # Sort hours from least crowded to most crowded
    average_occupancy = average_occupancy.sort_values()

    # Return the three least crowded hours
    return average_occupancy.head(3)
