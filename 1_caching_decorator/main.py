# -*- coding: utf-8 -*-

from collections import deque
from functools import wraps

def cache_with_limit(depth):
    def decorator(func):
        cache = {}
        call_order = deque(maxlen=depth)  # Хранит порядок вызовов для соблюдения глубины кэша

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Создаем ключ для кэша на основе аргументов
            key = (args, frozenset(kwargs.items()))

            if key in cache:
                print(f"Result for {args} was taken from cache")
                return cache[key]

            # Если результат не в кэше, выполняем функцию
            result = func(*args, **kwargs)

            # Если кэш переполнен, удаляем самый старый вызов
            if len(call_order) == depth:
                oldest_key = call_order.popleft()
                del cache[oldest_key]

            # Сохраняем результат в кэш
            cache[key] = result
            call_order.append(key)

            return result

        return wrapper

    return decorator

# Пример использования декоратора с глубиной кэша 3
@cache_with_limit(3)
def slow_function(x):
    return x * x

@cache_with_limit(3)
def slowest_function(x,y):
    return x * y

@cache_with_limit(3)
def absolut_slowest_function(x,y,z):
    return x * y * z

print(slow_function(2))  # Вычисляется и кэшируется
print(slow_function(2))  # Берется из кэша
print(slow_function(3))  # Вычисляется и кэшируется
print(slow_function(4))  # Вычисляется и кэшируется
print(slow_function(5))  # Вычисляется и кэшируется, кэш для 2 удаляется
print(slow_function(2))  # Повторное вычисление, так как результат был удален из кэша
print(slow_function(5))  # Вычисляется и кэшируется, кэш для 2 удаляется
print(slowest_function(2,3))
print(slowest_function(2,3))
print(absolut_slowest_function(2,3,4))
print(absolut_slowest_function(2,3,4))
