from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_AS_ASCII'] = False
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    with app.app_context():
        db.init_app(app)
        from . import routes
        db.create_all()

        from . import migrate
        migrate.load_users('data/users_data.json')
        migrate.load_orders('data/orders_data.json')
        migrate.load_offers('data/offers_data.json')

    return app
