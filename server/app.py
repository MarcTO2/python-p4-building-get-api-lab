#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Routes
@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    bakery_list = [bakery.to_dict() for bakery in all_bakeries]
    
    response = make_response(jsonify(bakery_list), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    specific_bakery = Bakery.query.filter_by(id=id).first()
    if specific_bakery:
        bakery_dict = specific_bakery.to_dict()
        response = make_response(jsonify(bakery_dict), 200)
    else:
        response = make_response(jsonify({'message': 'Bakery not found'}), 404)
    
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [bg.to_dict() for bg in baked_goods]
    
    response = make_response(jsonify(baked_goods_list), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        most_expensive_dict = most_expensive.to_dict()
        response = make_response(jsonify(most_expensive_dict), 200)
    else:
        response = make_response(jsonify({'message': 'No baked goods found'}), 404)
    
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
