from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Lkey884'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kiama:kiamapwd@localhost/Pitches'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from .models import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


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


if __name__ == '__main__':
    app.debug = True
    app.run()
