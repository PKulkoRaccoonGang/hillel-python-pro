import psutil
import functools
import requests


def measure_memory_usage(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        result = func(*args, **kwargs)
        final_memory = process.memory_info().rss
        memory_used = final_memory - initial_memory
        print(f'Function {func.__name__} used {memory_used} bytes of memory')
        return result

    return wrapper


@measure_memory_usage
def fetch_url(url, first_n=100):
    """Fetch the content of the given URL, returning the first N bytes"""
    response = requests.get(url)
    return response.content[:first_n] if first_n else response.content


fetch_url("https://ithillel.ua/")
