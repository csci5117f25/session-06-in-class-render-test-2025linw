from flask import Flask, request
from flask import render_template

from utils import convert_dict_keys_to_camelCase
from db import setup, get_db_cursor


app = Flask(__name__)

with app.app_context():
    setup()

"""
Pages
"""
@app.route('/')
def main():
    guest_list = query_guests()

    return render_template('main.html', guest_list=guest_list)

"""
API
"""
@app.route('/api/guests', methods=["GET"])
def get_guests():
    return query_guests()

@app.route('/api/guests', methods=["POST"])
def add_guest():
    # Body Format: { name: string, }
    body = dict(request.get_json())

    with get_db_cursor(commit=True) as curs:
        curs.execute("INSERT INTO session06.guestlist (guest_name) VALUES (%s) RETURNING *;", (body.get("guest_name"),))

        data = curs.fetchone()

    return convert_dict_keys_to_camelCase(dict(data)), 201

"""
DB
"""
def query_guests():
    with get_db_cursor() as curs:
        curs.execute("SELECT * FROM session06.guestlist ORDER BY created_at DESC;")

        data = curs.fetchall()

    return list(map(convert_dict_keys_to_camelCase, map(dict, data)))
