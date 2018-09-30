from faker import Faker
from flask import render_template, request, redirect, url_for, Blueprint, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_babel import _

from application.extensions import db
from application.models import User, Item

auth_bp = Blueprint("auth", __name__)
fake = Faker()


@auth_bp.route("/login", methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("todo.application"))

    if request.method == "POST":
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        user = User.query.filter_by(username=username).first()

        if user is not None and user.validate_password(password):
            login_user(user)
            return jsonify(message=_("login success"))
        return jsonify(message=_("Invalid credentials")), 400
    return render_template("_login.html")


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(message=_("Logout Success"))


@auth_bp.route('/register')
def register():
    # generate a random account for demo use
    username = fake.user_name()
    # make sure the generated username is not in the database
    while User.query.filter_by(username=username).first() is not None:
        username = fake.user_name()
    password = fake.word()
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    item = Item(body="!!!!!!!", author=user)
    item2 = Item(body="ddd", author=user)

    db.session.add_all([item, item2])
    db.session.commit()

    return jsonify(username=username, password=password, message=_("Generate success."))




