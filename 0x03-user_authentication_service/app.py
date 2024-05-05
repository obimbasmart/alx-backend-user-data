#!/usr/bin/env python3

"""Basic flask app"""

from flask import Flask, jsonify, request, make_response

from auth import Auth


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
