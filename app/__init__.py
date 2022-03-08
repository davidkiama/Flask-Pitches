from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

from .config import config_options


app = Flask(__name__)


app.config['SECRET_KEY'] = 'Lkey884'
app.config['SQLALCHEMY_DATABASE_URI'] = 'database_uri goes here'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


UPLOAD_FOLDER = 'app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
migrate = Migrate(app, db)

mail = Mail(app)

from .models import User


def create_app(config_name):

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    app.config.from_object(config_options[config_name])

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is the primary key, we use it to query
        return User.query.get(int(user_id))

        # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of the app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
