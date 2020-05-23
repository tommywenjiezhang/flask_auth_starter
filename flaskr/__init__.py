from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_login import LoginManager
def create_app():
    app = Flask(__name__,instance_relative_config=False)


    login_manager = LoginManager()
    login_manager.login_view = "auth.auth_bp"
    login_manager.init_app(app)

   


    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    from .model import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        from .home import home
        from .auth import auth
        app.register_blueprint(home.home_bp, url_prefix='/home')
        app.register_blueprint(auth.auth_bp)
        
    return app