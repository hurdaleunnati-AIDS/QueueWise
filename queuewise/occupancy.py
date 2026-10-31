
from config import LOW_LIMIT, MODERATE_LIMIT


def calculate_occupancy(previous_occupancy, entries, exits):
    # Check that all values are integers
    values = [previous_occupancy, entries, exits]

    for value in values:
        if type(value) is not int:
            raise ValueError("All values must be integers.")

    # Check for negative values
    if previous_occupancy < 0 or entries < 0 or exits < 0:
        raise ValueError("Values cannot be negative.")

    # Calculate new occupancy
    new_occupancy = previous_occupancy + entries - exits

    if new_occupancy < 0:
        raise ValueError("Exits cannot exceed the available occupancy.")

    return new_occupancy


def classify_crowd(occupancy, capacity):
    # Validate input
    if type(occupancy) is not int or type(capacity) is not int:
        raise ValueError("Occupancy and capacity must be integers.")

    if occupancy < 0 or capacity <= 0:
        raise ValueError("Invalid occupancy or capacity.")

    # Calculate occupancy percentage
    percentage = occupancy / capacity

    # Classify crowd level
    if percentage <= LOW_LIMIT:
        return "Low"
    elif percentage <= MODERATE_LIMIT:
        return "Moderate"
    else:
        return "High"
