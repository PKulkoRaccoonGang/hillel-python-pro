import httpx


def generate_user_data(faker_instance, number_of_users):
    """
    Generates a list of user data with random details.
    """
    users = []
    for _ in range(number_of_users):
        user = {
            'first_name': faker_instance.first_name(),
            'last_name': faker_instance.last_name(),
            'email': faker_instance.email(),
            'password': faker_instance.password(),
            'birthday': faker_instance.date_of_birth(minimum_age=18, maximum_age=60)
        }
        users.append(user)
    return users


def filter_by_code(data, code):
    """Filter the data by a specific currency code."""
    return next((entry for entry in data if entry['code'] == code), None)


def fetch_data(url):
    """Fetch data from a given URL and return the JSON response or raise an exception."""
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()


def get_currency_symbol(currencies, code):
    """Retrieve the symbol for a specific currency code."""
    currency = next((cur for cur in currencies if cur.get('code') == code.upper()), None)
    return currency.get('symbol', '') if currency else ''
