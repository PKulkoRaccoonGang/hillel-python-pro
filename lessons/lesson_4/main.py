from http import HTTPStatus
from flask import Flask, jsonify, render_template, abort, send_file, Response


app = Flask(__name__)


@app.errorhandler(HTTPStatus.NOT_FOUND)
def error_handling(error):
  headers = error.data.get('headers', None)
  messages = error.data.get('messages', ['Invalid request.'])
  
  if headers:
    return jsonify({ 'errors': messages }, error.code, headers)
  return jsonify({ 'errors': messages }, error.code)


@app.route('/admin/<int:count>')
def hello_world(count) -> str:
    return f'Hello, World - {count}!'


if __name__ == '__main__':
    app.run(port=5003, debug=True)
