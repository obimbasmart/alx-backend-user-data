#!/usr/bin/env python3

"""Basic flask app"""

from flask import Flask, jsonify, request

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
