import datetime

from . import db


def instance_to_dict(instance: db.Model) -> dict:
    """Convert an instance of db.Model class to dict"""
    result = {c.name: getattr(instance, c.name) for c in instance.__table__.columns}
    return result


def string_to_date(date_string: str, format_string: str = None) -> datetime.date:
    """Convert date from a string to a date object"""
    if format_string is None:
        format_string = '%m/%d/%Y'

    date = datetime.datetime.strptime(date_string, format_string).date()
    return date
