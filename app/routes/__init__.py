from app.routes.user_blueprint import bp as bp_user

def init_app(app):
    app.register_blueprint(bp_user)