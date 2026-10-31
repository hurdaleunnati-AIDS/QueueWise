
from datetime import datetime


def validate_reading(entries, exits, observed_at):

    # Entries and exits must be integers
    if type(entries) is not int or type(exits) is not int:
        return False

    # Counts cannot be negative
    if entries < 0 or exits < 0:
        return False

    # Timestamp must be a datetime object
    if not isinstance(observed_at, datetime):
        return False

    # Future timestamps are not allowed
    if observed_at > datetime.now():
        return False

    return True
