import os
import httpx
from http import HTTPStatus

from flask import Flask, render_template, abort, send_file, Response
from faker import Faker
from webargs.flaskparser import use_kwargs
import pandas as pd

from settings import CSV_FILE_PATH, BASE_CURRENCY_URL
from validators import number_of_users_config, bitcoin_search_config
from utils import generate_user_data, fetch_data, filter_by_code, get_currency_symbol


app = Flask(__name__)


@app.route('/generate-students')
@use_kwargs(number_of_users_config, location='query')
def generate_students(number_of_users):
    """
    Generates a specified number of student records, saves them to a CSV file, 
    and renders a web page displaying the generated records.
    """
    faker_instance = Faker()
    users = generate_user_data(faker_instance, number_of_users)
    
    try:
        data_frame = pd.DataFrame(users)
        data_frame.to_csv(CSV_FILE_PATH, index=False)
    except Exception as e:
        abort(500, description=f'Error saving CSV: {e}')
    
    return render_template('users.html', users=users)


@app.route('/download-csv')
def download_csv():
    """
    Handles the download of the generated CSV file.
    """
    if os.path.exists(CSV_FILE_PATH):
        return send_file(CSV_FILE_PATH, as_attachment=True)
    else:
        abort(404, description='CSV file not found.')


@app.route('/get-bitcoin-value/bitcoin_rate')
@use_kwargs(bitcoin_search_config, location='query')
def get_bitcoin_value(currency, amount_of_currency):
    """Fetch the Bitcoin value for a specified currency and conversion rate."""
    try:
        rates_data = fetch_data(f'{BASE_CURRENCY_URL}/api/rates')
        currencies_data = fetch_data(f'{BASE_CURRENCY_URL}/currencies').get('data', [])
        
        filtered_currency_data = filter_by_code(rates_data, currency)
        if not filtered_currency_data:
            return Response(f'ERROR: Currency {currency} not found.', status=HTTPStatus.BAD_REQUEST)
        
        total_amount_of_currency = amount_of_currency * filtered_currency_data['rate']
        currency_symbol = get_currency_symbol(currencies_data, currency)
        
        context = {
            'filtered_currency_date': filtered_currency_data,
            'total_amount_of_currency': total_amount_of_currency,
            'currency_symbol': currency_symbol
        }
        return render_template('crypto_currency.html', **context)
    
    except httpx.HTTPStatusError as e:
        return Response(f'ERROR: Failed to fetch data from the API. {str(e)}', status=HTTPStatus.BAD_REQUEST)
    except TypeError as e:
        return Response(f'ERROR: Data format issue. {str(e)}', status=HTTPStatus.INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response(f'ERROR: An unexpected error occurred. {str(e)}', status=HTTPStatus.INTERNAL_SERVER_ERROR)


if __name__ == '__main__':
    app.run(port=5002, debug=True)
