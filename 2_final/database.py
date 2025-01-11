from dataclasses import dataclass
from datetime import date
from decimal import *

@dataclass
class Price:
    item_id: int
    date: date
    price: Decimal

def database_init():
    pass

def database_get_user_id(telegram_handle):
    pass

def database_get_item_id(item_name):
    pass

def database_get_subscribed_item_ids(user_id):
    pass

def database_get_unsubscribed_item_ids(user_id):
    pass

def database_get_item_name(item_id):
    pass

def database_add_subscription(user_id, item_name):
    pass

def database_remove_subscription(user_id, item_name):
    pass

def database_get_prices_of_item_for_n_days(item_id, n_days):
    pass
