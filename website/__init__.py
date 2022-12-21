from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db=SQLAlchemy()
DB_NAME = "database.db"

# create a flask app
def create_app():

    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'a random string'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # add those different files to app
    from .views import views
    from .auth import auth
    # register those blueprint(s)
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # creating database
    # models are imported from models.py
    from .models import User, Note
    # create_database(app)

    # with app.app_context():
    #     db.create_all()
    # run this one time two lines above when first running app
    

    login_manager=LoginManager()
    login_manager.login_view='auth.login' # redirect to login page if you are not logged in
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app



# deprecated
# def create_database(application):

#     if not path.exists(f"website/{DB_NAME}"):
#         with application.app_context():
#             db.create_all()
#             print("Databse created!")