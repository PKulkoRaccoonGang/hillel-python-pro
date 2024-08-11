import secrets
import string

import pandas as pd
from flask import Flask, abort

from config import MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH, AVAILABLE_CHARACTERS, columns_to_average
from utils import clean_column_names


app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


@app.route('/hello')
def hello_mykhailo():
    return "<p>Hello, Mykhailo!</p>"


@app.route('/generate_password')
def generate_password() -> str:
    """
    from 10 to 20 chars
    upper and lower case
    """
    password_length = secrets.randbelow(MAX_PASSWORD_LENGTH - MIN_PASSWORD_LENGTH + 1) + MIN_PASSWORD_LENGTH
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation)
    ]
    password += [secrets.choice(AVAILABLE_CHARACTERS) for _ in range(password_length - 4)]
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)


@app.route('/avarage_statistics')
def calculate_average(filename='flask_hw_2.csv'):
    """
    csv file with students
    1.calculate average high
    2.calculate average weight
    """
    try:
        data_frame = pd.read_csv(filename)
        formatted_data_frame = clean_column_names(data_frame)
        average_values = {col: formatted_data_frame[col].mean() for col in columns_to_average}
        list_items = ''.join(
            f'<li>Average {col}: <b>{average_values[col]:.2f}</b></li>' for col in columns_to_average
        )
        return f'<ol>{list_items}</ol>'
    except FileNotFoundError:
        return abort(404, description='File not found.')
    except pd.errors.EmptyDataError:
        return abort(400, description='CSV file is empty.')
    except KeyError as e:
        missing_column = str(e).strip("'")
        return abort(400, description=f'Missing "{missing_column}" column in the CSV file.')
    except Exception as e:
        return abort(500, description=f'An unexpected error occurred: {str(e)}')


app.run(port=5001, debug=True)
