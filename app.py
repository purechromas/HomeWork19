from flask import Flask
from flask_restx import Api

from config import Config
from setup_db import db
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import user_ns
from views.auth import auth_ns
from dao.model.user import User
from implemented import user_service


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)


app = create_app(Config())


u1 = User(username="Vasya", password=user_service.create_hash_password("my_little_pony"), role="user")
u2 = User(username="Oleg", password=user_service.create_hash_password("qwerty"), role="user")
u3 = User(username="Blagovest", password=user_service.create_hash_password("my_big_horse"), role="admin")

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add_all([u1, u2, u3])
    db.session.commit()


if __name__ == '__main__':
    app.run()
