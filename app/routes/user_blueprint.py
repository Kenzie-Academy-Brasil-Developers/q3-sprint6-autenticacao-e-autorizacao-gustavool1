from flask import Blueprint

from app.controllers.user_controller import create_user, login, get_user,update_user, delete_user

bp = Blueprint("user_blueprint", __name__, url_prefix = "/api")

bp.post("/signup")(create_user)
bp.post("/signin")(login)
bp.get("")(get_user)
bp.patch("")(update_user)
bp.delete("")(delete_user)