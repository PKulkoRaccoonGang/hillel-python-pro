import functools
import requests

from collections import OrderedDict


def lfu_cache(max_size=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            if cache_key in wrapper._cache:
                wrapper._cache.move_to_end(cache_key, last=True)
                cache_item = wrapper._cache[cache_key]
                cache_item['usage_count'] += 1
                return cache_item['result']
            result = func(*args, **kwargs)
            new_cache_item = {'result': result, 'usage_count': 1}
            if len(wrapper._cache) >= max_size:
                extra_key = min(wrapper._cache.items(), key=lambda item: item[1]['usage_count'])[0]
                del wrapper._cache[extra_key]
            wrapper._cache[cache_key] = new_cache_item
            return result

        wrapper._cache = OrderedDict()
        return wrapper

    return decorator


@lfu_cache()
def fetch_url(url, first_n=100):
    """Fetch content from a given URL"""
    response = requests.get(url)
    return response.content[:first_n] if first_n else response.content

fetch_url('https://rozetka.com.ua/')
fetch_url('https://rozetka.com.ua/')
fetch_url('https://rozetka.com.ua/')
fetch_url('https://ithillel.ua/')
fetch_url('https://rozetka.com.ua/')
fetch_url('https://ithillel.ua/')
fetch_url('https://ithillel.ua/')
fetch_url('https://ithillel.ua/')
fetch_url('https://www.javascript.com/')
fetch_url('https://www.javascript.com/')
fetch_url('https://www.javascript.com/')
fetch_url('https://ithillel.ua/')
fetch_url('https://rozetka.com.ua/')
fetch_url('https://www.github.com/')
fetch_url('https://www.github.com/')
fetch_url('https://www.github.com/')
fetch_url('https://www.github.com/')
fetch_url('https://www.github.com/')
fetch_url('https://www.github.com/')
