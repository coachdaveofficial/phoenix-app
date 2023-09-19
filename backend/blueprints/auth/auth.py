from functools import wraps
from flask import Blueprint, jsonify, make_response, request, flash, redirect, g, session
from services import UserService
from models import User
from flask_cors import cross_origin

auth_bp = Blueprint("auth", __name__)
CURR_USER_KEY = "curr_user"

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return make_response({"message": "You are not authorized to access this page"}, 401)
        return view_func(*args, **kwargs)
    return wrapped_view

@auth_bp.route('/@me', methods=["GET"])
@cross_origin(supports_credentials=True)
def get_current_user():
    user_id = session.get(CURR_USER_KEY)
    print(session)

    if not user_id:
        return make_response({"message": "You are not authorized to access this page"}, 401)
    
    user = User.query.get(user_id)
    print(user, "test")
    

    return jsonify({"id": user.id, "username": user.username})


@auth_bp.route('/signup/', methods=["POST"])
def signup():
    signup_data = request.get_json()
    username = signup_data.get("username")
    password = signup_data.get("password")
    email = signup_data.get("email")


    user = UserService.signup(username, email, password)

    if not user:
        return make_response(jsonify({"message": "Error creating user. Username or Email already taken"}), 400)
    
    do_login(user)
    return make_response(jsonify({"message": "Succesfully created new user"}), 201)


@auth_bp.route('/login/', methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    login_data = request.get_json()
    username = login_data.get("username")
    password = login_data.get("password")

    user = UserService.authenticate(username, password)
    if not user:
        return make_response(jsonify({"message": "Invalid username or password. Please try again"}), 401)
    do_login(user)
    return make_response(jsonify({"message": "Login successful"}), 200)

@auth_bp.route('/logout/', methods=["GET"])
def logout():
    """Handle logout of user."""
    

    do_logout()
    return make_response(jsonify({"message": "Successfully logged out"}), 200)
