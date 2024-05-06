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
    """add a new user"""
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
    """login a user"""
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
    """logout a user"""
    session_id = request.cookies.get("session_id")
    try:
        user = AUTH._db.find_user_by(session_id=session_id)
        AUTH.destroy_session(user.id)
        redirect("/")
    except NoResultFound as err:
        abort(403)


@app.route("/profile")
def profile():
    """get user profile"""
    session_id = request.cookies.get("session_id")
    try:
        user = AUTH._db.find_user_by(session_id=session_id)
        return jsonify({"email": user.email}), 200
    except NoResultFound as err:
        abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """get reset token"""
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """update password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
