from flask import current_app as app, jsonify, request
from sqlalchemy.orm.exc import UnmappedInstanceError

from . import models, db
from .utils import instance_to_dict, string_to_date


@app.get('/users')
def all_users():
    users = models.User.query.all()
    users_list = [instance_to_dict(u) for u in users]
    return jsonify(users_list)


@app.post('/users')
def add_user():
    user_data = request.json

    try:
        user_object = models.User(**user_data)
    except TypeError:
        return 'Invalid JSON', 400

    with db.session.begin():
        db.session.add(user_object)
    return jsonify('Added successfully')


@app.get('/users/<int:uid>')
def user_by_id(uid):
    user = models.User.query.get(uid)

    if not user:
        return jsonify('No such user'), 404

    user_dict = instance_to_dict(user)
    return jsonify(user_dict)


@app.put('/users/<int:uid>')
def update_user(uid):
    user: models.User = models.User.query.get(uid)
    if not user:
        return jsonify('No such user'), 404

    new_user_data = request.json

    try:
        user.first_name = new_user_data['first_name']
        user.last_name = new_user_data['last_name']
        user.email = new_user_data['email']
        user.age = new_user_data['age']
        user.phone = new_user_data['phone']
        user.role = new_user_data['role']
    except KeyError:
        return 'Invalid JSON', 400

    db.session.add(user)
    db.session.commit()
    return jsonify('Updated successfully')


@app.delete('/users/<int:uid>')
def delete_user(uid):
    try:
        with db.session.begin():
            user = models.User.query.get(uid)
            db.session.delete(user)
    except UnmappedInstanceError:
        return jsonify('No user with this id'), 404

    return jsonify('Deleted successfully')


@app.get('/orders')
def all_orders():
    orders = models.Order.query.all()
    orders_list = [instance_to_dict(o) for o in orders]
    return jsonify(orders_list)


@app.get('/orders/<int:oid>')
def order_by_id(oid):
    order = models.Order.query.get(oid)
    order_dict = instance_to_dict(order)
    return jsonify(order_dict)


@app.post('/orders')
def add_order():
    order_data = request.json

    try:
        order_data['start_date'] = string_to_date(order_data['start_date'])
        order_data['end_date'] = string_to_date(order_data['end_date'])
        order_object = models.Order(**order_data)
    except (TypeError, KeyError):
        return 'Invalid JSON', 400

    with db.session.begin():
        db.session.add(order_object)
    return jsonify('Added successfully')


@app.put('/orders/<int:oid>')
def update_order(oid):
    order: models.Order = models.Order.query.get(oid)
    if not order:
        return jsonify('No such order'), 404

    new_order_data = request.json

    try:
        order.name = new_order_data['name']
        order.description = new_order_data['description']
        order.address = new_order_data['address']
        order.price = new_order_data['price']
        order.customer_id = new_order_data['customer_id']
        order.executor_id = new_order_data['executor_id']
        order.start_date = string_to_date(new_order_data['start_date'])
        order.end_date = string_to_date(new_order_data['end_date'])
    except KeyError:
        return 'Invalid JSON', 400

    db.session.add(order)
    db.session.commit()
    return jsonify('Updated successfully')


@app.delete('/orders/<int:oid>')
def delete_order(oid):
    try:
        with db.session.begin():
            order = models.Order.query.get(oid)
            db.session.delete(order)
    except UnmappedInstanceError:
        return jsonify('No order with this id'), 404

    return jsonify('Deleted successfully')


@app.get('/offers')
def all_offers():
    offers = models.Offer.query.all()
    offers_list = [instance_to_dict(o) for o in offers]
    return jsonify(offers_list)


@app.get('/offers/<int:oid>')
def offer_by_id(oid):
    offer = models.Offer.query.get(oid)
    offer_dict = instance_to_dict(offer)
    return jsonify(offer_dict)


@app.post('/offers')
def add_offer():
    offer_data = request.json

    try:
        offer_object = models.Offer(**offer_data)
    except TypeError:
        return 'Invalid JSON', 400

    with db.session.begin():
        db.session.add(offer_object)
    return jsonify('Added successfully')


@app.put('/offers/<int:oid>')
def update_offer(oid):
    offer: models.Offer = models.Offer.query.get(oid)
    if not offer:
        return jsonify('No such offer'), 404

    new_offer_data = request.json

    try:
        offer.order_id = new_offer_data['order_id']
        offer.executor_id = new_offer_data['executor_id']
    except KeyError:
        return 'Invalid JSON', 400

    db.session.add(offer)
    db.session.commit()
    return jsonify('Updated successfully')


@app.delete('/offers/<int:oid>')
def delete_offer(oid):
    try:
        with db.session.begin():
            offer = models.Offer.query.get(oid)
            db.session.delete(offer)
    except UnmappedInstanceError:
        return jsonify('No offer with this id'), 404

    return jsonify('Deleted successfully')
