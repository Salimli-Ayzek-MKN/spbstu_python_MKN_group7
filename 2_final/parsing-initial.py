from dataclasses import dataclass
from datetime import date
from decimal import Decimal
import database;

@dataclass
class PriceChange:
    date: date
    price: Decimal
    price_change: Decimal

def get_subscribed(telegram_handle):
    user_id = database.get_user_id(telegram_handle)
    item_ids = database.get_subscribed_item_ids(user_id)
    return [database.get_item_name(item_id) for item_id in item_ids]

def get_unsubscribed(telegram_handle):
    user_id = database.get_user_id(telegram_handle)
    item_ids = database.get_unsubscribed_item_ids(user_id)
    return [database.get_item_name(item_id) for item_id in item_ids]

def subscribe(telegram_handle, item_name):
    user_id = database.get_user_id(telegram_handle)
    item_id = database.get_item_id(item_name)
    database.add_subscription(user_id, item_id)

def unsubscribe(telegram_handle, item_name):
    user_id = database.get_user_id(telegram_handle)
    item_id = database.get_item_id(item_name)
    database.remove_subscription(user_id, item_id)

def get_report(telegram_handle, n_days):
    user_id = database.get_user_id(telegram_handle)
    item_ids = database.get_subscribed_item_ids(user_id)
    price_changes = []
    for item_id in item_ids:
        item_name = database.get_item_name(item_id)
        price_changes[item_name] = []
        prices = database.get_prices_of_item_for_n_days(item_id, n_days)
        last_price = 0
        for price in prices:
            price_changes[item_name].append(
                PriceChange(price.date,
                            price.price,
                            price.price - last_price))
