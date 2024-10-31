# -*- coding: utf-8 -*-

from collections import deque
from functools import wraps

def cache_with_limit(depth):
    
    
    def decorator(func):
        cache = {}
        call_order = deque(maxlen=depth)  # ������ ������� ������� ��� ���������� ������� ����
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # ������� ���� ��� ���� �� ������ ����������
            key = (args, frozenset(kwargs.items()))
            
            if key in cache:
                print(f"Result for {args} was taken from cache")
                return cache[key]
            
            # ���� ��������� �� � ����, ��������� �������
            result = func(*args, **kwargs)
            
            # ���� ��� ����������, ������� ����� ������ �����
            if len(call_order) == depth:
                oldest_key = call_order.popleft()
                del cache[oldest_key]
            
            # ��������� ��������� � ���
            cache[key] = result
            call_order.append(key)
            
            return result
        
        return wrapper
    
    return decorator

# ������ ������������� ���������� � �������� ���� 3
@cache_with_limit(3)
def slow_function(x):
    return x * x

@cache_with_limit(3)
def slowest_function(x,y):
    return x * y

@cache_with_limit(3)
def absolut_slowest_function(x,y,z):
    return x * y * z

print(slow_function(2))  # ����������� � ����������
print(slow_function(2))  # ������� �� ����
print(slow_function(3))  # ����������� � ����������
print(slow_function(4))  # ����������� � ����������
print(slow_function(5))  # ����������� � ����������, ��� ��� 2 ���������
print(slow_function(2))  # ��������� ����������, ��� ��� ��������� ��� ������ �� ����
print(slow_function(5))  # ����������� � ����������, ��� ��� 2 ���������
print(slowest_function(2,3))
print(slowest_function(2,3))
print(absolut_slowest_function(2,3,4))
print(absolut_slowest_function(2,3,4))

