from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
import mysql.connector

@dataclass
class Price:
    item_id: int
    date: date
    price: Decimal

def database_init():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="pricebot"
    )

def database_get_user_id(telegram_handle):
    connection = database_init()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM users WHERE telegram_handle = %s", (telegram_handle,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

def database_get_item_id(item_name):
    connection = database_init()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM items WHERE name = %s", (item_name,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

def database_get_subscribed_item_ids(user_id):
    connection = database_init()
    cursor = connection.cursor()
    cursor.execute("SELECT id_item FROM subscriptions WHERE id_user = %s", (user_id,))
    result = cursor.fetchall()
    connection.close()
    return [row[0] for row in result]

def database_get_unsubscribed_item_ids(user_id):
    connection = database_init()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM items WHERE id NOT IN (SELECT id_item FROM subscriptions WHERE id_user = %s)", (user_id,))
    result = cursor.fetchall()
    connection.close()
    return [row[0] for row in result]

def database_get_item_name(item_id):
    connection = database_init()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM items WHERE id = %s", (item_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

def database_add_subscription(user_id, item_name):
    connection = database_init()
    cursor = connection.cursor()
    item_id = database_get_item_id(item_name)
    if item_id:
        cursor.execute("INSERT INTO subscriptions (id_user, id_item) VALUES (%s, %s)", (user_id, item_id))
        connection.commit()
    connection.close()

def database_remove_subscription(user_id, item_name):
    connection = database_init()
    cursor = connection.cursor()
    item_id = database_get_item_id(item_name)
    if item_id:
        cursor.execute("DELETE FROM subscriptions WHERE id_user = %s AND id_item = %s", (user_id, item_id))
        connection.commit()
    connection.close()

def database_get_prices_of_item_for_n_days(item_id, n_days):
    connection = database_init()
    cursor = connection.cursor()
    start_date = (date.today() - timedelta(days=n_days)).strftime('%Y-%m-%d')
    cursor.execute("SELECT date, price FROM item_prices WHERE id_item = %s AND date >= %s", (item_id, start_date))
    result = cursor.fetchall()
    connection.close()
    return [Price(item_id=item_id, date=row[0], price=Decimal(row[1])) for row in result]
