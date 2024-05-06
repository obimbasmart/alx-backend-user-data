#!/usr/bin/env python3

"""Basic flask app"""

from flask import (Flask, jsonify,
                   request, make_response,
                   abort, redirect)

from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def home():
    """index --"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["GET", "POST"])
def users():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": "<registered email>",
                        "message": "user created"}), 200
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = make_response(jsonify({"email": email, "message": "logged in"}))
        resp.set_cookie('session_id', session_id)
        return resp
    abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    session_id = request.cookies.get("session_id")
    try:
        user = AUTH._db.find_user_by(session_id=session_id)
        AUTH.destroy_session(user.id)
        redirect("/")
    except NoResultFound as err:
        abort(403)


@app.route("/profile")
def profile():
    session_id = request.cookies.get("session_id")
    try:
        user = AUTH._db.find_user_by(session_id=session_id)
        return jsonify({"email": user.email}), 200
    except NoResultFound as err:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
