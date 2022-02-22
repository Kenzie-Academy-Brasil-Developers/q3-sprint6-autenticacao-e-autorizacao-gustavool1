
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from flask import current_app, jsonify, request, session
from secrets import token_urlsafe
from app.models.user_model import UserModel
from app.configs.auth import auth
from werkzeug.exceptions import Unauthorized
def create_user():
    try:
        session = current_app.db.session
        data = request.get_json()
        data["api_key"] = token_urlsafe(16)

        user = UserModel(**data)
        session.add(user)
        session.commit()
        return jsonify(user), HTTPStatus.CREATED

    except IntegrityError:
        return {"msg":"This email already exists"}, HTTPStatus.CONFLICT



def login():
    data = request.get_json()

    user = UserModel.query.filter(UserModel.email == data["email"]).first()

    if not user:
        return {"msg": "This email doenst exists"}, HTTPStatus.NOT_FOUND

    if user.check_password(data["password"]):
        return {"api_key": user.api_key}, HTTPStatus.OK

    
    return {"msg":"Account not found"}, HTTPStatus.NOT_FOUND



@auth.login_required
def get_user():
    api_key = request.headers["Authorization"].split()[1]
    user = UserModel.query.filter_by(api_key = api_key).first()
    return jsonify(user), HTTPStatus.OK
    

@auth.login_required
def update_user():
    session = current_app.db.session
    valid_fields = ["name", "last_name", "email", "password"]
    data = request.get_json()

    api_key = request.headers["Authorization"].split()[1]
    user = UserModel.query.filter_by(api_key = api_key).first()

    for key,value in data.items():
        if key in valid_fields:
            setattr(user, key, value)

    session.add(user)
    session.commit()

    return jsonify(user), HTTPStatus.OK


@auth.login_required
def delete_user():
    session = current_app.db.session
    api_key = request.headers["Authorization"].split()[1]

    user = UserModel.query.filter_by(api_key=api_key).first()

    session.delete(user)
    session.commit()

    return { "msg": f"User {user.name} has been deleted."}, HTTPStatus.OK