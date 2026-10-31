
from datetime import datetime, timedelta

from queuewise.database import insert_reading, get_reading_count
from queuewise.validation import validate_reading
from queuewise.occupancy import calculate_occupancy


def load_demo_data():

    # Avoid inserting the same demo records repeatedly
    if get_reading_count() > 0:
        return

    # Example occupancy values for 24 hours
    occupancy_values = [
        20, 15, 12, 10, 8, 12,
        25, 40, 55, 70, 85, 95,
        110, 120, 115, 100, 90, 75,
        65, 55, 45, 35, 30, 25
    ]

    previous_occupancy = 0

    for hour in range(24):

        current_occupancy = occupancy_values[hour]

        # Calculate entries and exits
        difference = current_occupancy - previous_occupancy

        if difference >= 0:
            entries = difference
            exits = 0
        else:
            entries = 0
            exits = abs(difference)

        # Calculate timestamp
        observed_at = datetime.now() - timedelta(hours=23 - hour)

        # Validate the record
        if validate_reading(entries, exits, observed_at):

            # Calculate occupancy
            occupancy = calculate_occupancy(
                previous_occupancy,
                entries,
                exits
            )

            # Save record in database
            insert_reading(
                observed_at.isoformat(timespec="seconds"),
                entries,
                exits,
                occupancy,
                "Demo generator",
                "DEMO"
            )

        previous_occupancy = current_occupancy
