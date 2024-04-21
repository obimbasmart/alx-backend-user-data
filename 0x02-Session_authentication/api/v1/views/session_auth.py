#!/usr/bin/env python3


""" Session authentication views
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route("/auth_session/login",
                 strict_slashes=False,
                 methods=["POST"])
def login():
    """login user"""
    email = request.form.get("email")
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if password is None:
        return jsonify({"error": "password missing"}), 400

    user_list = User.search({"email": email})
    user = user_list[0] if len(user_list) else None

    if user is None:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = make_response(jsonify(user.to_json()))
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response


@app_views.route("/auth_session/logout",
                 strict_slashes=False,
                 methods=["DELETE"])
def logout():
    """logout user"""
    from api.v1.app import auth
    res = auth.destroy_session(request)
    if not res:
        abort(404)
    return jsonify({}), 200
