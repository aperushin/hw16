import json

from . import models, db
from .utils import string_to_date


def load_json(filename: str) -> list | dict:
    with open(filename, encoding="utf8") as f:
        json_data = json.load(f)
    return json_data


def load_users(filename: str) -> None:
    """Add users to database"""
    users_data = load_json(filename)
    users = [models.User(**u) for u in users_data]
    with db.session.begin():
        db.session.add_all(users)


def load_orders(filename: str) -> None:
    """Add orders to database"""
    orders_data = load_json(filename)
    orders = []

    for o in orders_data:
        o['start_date'] = string_to_date(o['start_date'])
        o['end_date'] = string_to_date(o['end_date'])
        orders.append(models.Order(**o))

    with db.session.begin():
        db.session.add_all(orders)


def load_offers(filename: str) -> None:
    """Add offers to database"""
    offers_data = load_json(filename)
    offers = [models.Offer(**of) for of in offers_data]

    with db.session.begin():
        db.session.add_all(offers)
