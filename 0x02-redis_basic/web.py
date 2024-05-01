#!/usr/bin/env python3
""" Expiring web cache module """

import redis
import requests
from typing import Callable
from functools import wraps

redis_conn = redis.Redis()

def wrap_requests(fn: Callable) -> Callable:
    """ Decorator wrapper """

    @wraps(fn)
    def wrapper(url):
        """ Wrapper for decorated function """
        redis_conn.incr(f"count:{url}")
        cached_response = redis_conn.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')
        result = fn(url)
        redis_conn.setex(f"cached:{url}", 10, result)
        return result

    return wrapper

@wrap_requests
def get_page(url: str) -> str:
    """ Fetches a web page and caches it """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    """Example usage"""
    print(get_page("http://slowwly.robertomurray.co.uk"))
