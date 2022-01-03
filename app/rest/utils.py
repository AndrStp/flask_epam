from datetime import datetime
from typing import TypeVar, Tuple, Optional


DATE = TypeVar('DATE', bound=datetime)


def time_validation(date_from: str, date_to: str) -> Tuple[Optional[DATE],
                                                           Optional[DATE]]:
    """
    Ensures that passed str objects can be transformed
    to datetime objects. Uses datetime.strptime func.
    Expects "%Y-%m-%d" format.

    :param date_from: str
    :param date_to: str
    :returns: tuple of either two datetime objects
    or None and datetime object
    """
    if date_from and date_to:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        except ValueError:
            date_from = None

        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            date_to = None

        return date_from, date_to

    if not date_to:
        date_to = datetime.date(datetime.utcnow())
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        except ValueError:
            date_from = None


    if not date_from:
        date_from = datetime(2021, 12, 1).date()
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            date_to = None

    return date_from, date_to
