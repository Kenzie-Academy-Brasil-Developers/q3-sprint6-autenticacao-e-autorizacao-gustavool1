
import email
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from flask import current_app, jsonify, request, session
from secrets import token_urlsafe
from app.models.user_model import UserModel
from app.configs.auth import auth
from flask_jwt_extended import create_access_token, jwt_required, decode_token


def create_user():
    try:
        session = current_app.db.session
        data = request.get_json()

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
        token = create_access_token(user)
        return {"acess_token": token}, HTTPStatus.OK

    
    return {"msg":"Account not found"}, HTTPStatus.NOT_FOUND



@jwt_required()
def get_user():
    token = request.headers["Authorization"].split()[1]
    user = decode_token(token)["sub"]
    return jsonify(user), HTTPStatus.OK
    

@jwt_required()
def update_user():
    session = current_app.db.session
    valid_fields = ["name", "last_name", "email", "password"]
    data = request.get_json()

    token = request.headers["Authorization"].split()[1]
    user_email = decode_token(token)["sub"]["email"]

    user = UserModel.query.filter_by(email = user_email).first()

    for key,value in data.items():
        if key in valid_fields:
            setattr(user, key, value)

    session.add(user)
    session.commit()

    return jsonify(user), HTTPStatus.OK


@jwt_required()
def delete_user():
    session = current_app.db.session
    token  = request.headers["Authorization"].split()[1]
    user_email = decode_token(token)["sub"]["email"]
    user = UserModel.query.filter_by(email=user_email).first()

    session.delete(user)
    session.commit()

    return { "msg": f"User {user.name} has been deleted."}, HTTPStatus.OK