from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth

from flask import Flask, request, session
from flask import render_template, redirect, url_for, flash

from utils import convert_dict_keys_to_camelCase
from db import setup, get_db_cursor


app = Flask(__name__)
app.static_folder = "static"
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

with app.app_context():
    setup()

"""
Pages
"""
@app.route("/")
def main():
    guest_list = query_guests()

    return render_template("main.html", guest_list=guest_list)

@app.route("/admin")
def admin():
    if "user" not in session:
        flash("User session not found, please login!")

        return redirect(url_for("main"))

    guest_list = query_guests()

    return render_template("admin.html", guest_list=guest_list)

"""
API
"""
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()

    session["user"] = token

    return redirect(url_for("main"))

@app.route("/logout")
def logout():
    session.clear()

    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("main", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/api/guests", methods=["GET"])
def get_guests():
    return query_guests()

@app.route("/api/guests", methods=["POST"])
def add_guest():
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

@app.delete("/api/guests/<guestId>")
def delete_guest(guestId):
    try:
        with get_db_cursor(commit=True) as curs:
            curs.execute("DELETE FROM session06.guestlist WHERE id=%s", (guestId,))
    except Exception as e:
        print(e)
        return "", 500

    return "", 204
