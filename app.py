import datetime

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import UnmappedInstanceError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    # orders = relationship('Order')
    # offers = relationship('Offer')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(200))
    price = db.Column(db.Float)
    customer_id = db.Column(db.ForeignKey('users.id'))
    executor_id = db.Column(db.ForeignKey('users.id'))

    # users = relationship('User')


class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.ForeignKey('orders.id'))
    executor_id = db.Column(db.ForeignKey('users.id'))

    # users = relationship('User')
    # orders = relationship('Order')


def instance_to_dict(instance: db.Model) -> dict:
    """Convert an instance of db.Model class to dict"""
    result = {c.name: getattr(instance, c.name) for c in instance.__table__.columns}
    return result


@app.get('/users')
def all_users():
    users = User.query.all()
    users_list = [instance_to_dict(u) for u in users]
    return jsonify(users_list)


@app.post('/users')
def add_user():
    user_data = request.json

    try:
        user_object = User(**user_data)
        with db.session.begin():
            db.session.add(user_object)
    except TypeError:
        return 'Invalid JSON', 400

    return jsonify('Added successfully')


@app.get('/users/<int:uid>')
def user_by_id(uid):
    user = User.query.get(uid)

    if not user:
        return jsonify('No such user'), 404

    user_dict = instance_to_dict(user)
    return jsonify(user_dict)


@app.put('/users/<int:uid>')
def update_user(uid):
    if not User.query.get(uid):
        return jsonify('No such user'), 404

    user_data = request.json

    try:
        with db.session.begin():
            user_object = User(**user_data)
            user_object.id = uid
            db.session.add(user_object)
    except TypeError:
        return 'Invalid JSON', 400

    return jsonify('Added successfully')


@app.delete('/users/<int:uid>')
def delete_user(uid):
    try:
        with db.session.begin():
            user = User.query.get(uid)
            db.session.delete(user)
    except UnmappedInstanceError:
        return jsonify('No user with this id'), 404

    return jsonify('Deleted successfully')


@app.get('/orders')
def all_orders():
    orders = Order.query.all()
    orders_list = [instance_to_dict(o) for o in orders]
    return jsonify(orders_list)


@app.get('/orders/<int:oid>')
def order_by_id(oid):
    order = Order.query.get(oid)
    order_dict = instance_to_dict(order)
    return jsonify(order_dict)


@app.get('/offers')
def all_offers():
    offers = Offer.query.all()
    offers_list = [instance_to_dict(o) for o in offers]
    return jsonify(offers_list)


@app.get('/offers/<int:oid>')
def offer_by_id(oid):
    offer = Offer.query.get(oid)
    offer_dict = instance_to_dict(offer)
    return jsonify(offer_dict)


if __name__ == '__main__':
    app.run(debug=True)
