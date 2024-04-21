#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os
from sqlalchemy.orm import Session

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_data = []

    for restaurant in restaurants:
        restaurant_info = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        }
        restaurant_data.append(restaurant_info)

    return jsonify(restaurant_data), 200



@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if restaurant:
        restaurant_dict = restaurant.to_dict()
        return jsonify(restaurant_dict), 200
    else:
        return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return jsonify({'message': 'Restaurant deleted successfully'}), 204
    else:
        return jsonify({'error': 'Restaurant not found'}), 404
    
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_data = []

    for pizza in pizzas:
        pizza_info = {
            "id": pizza.id,
            "ingredients": pizza.ingredients,
            "name": pizza.name
        }
        pizza_data.append(pizza_info)

    return jsonify(pizza_data), 200


@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    if request.method == 'POST':

        data = request.json

        price = data.get("price")
        pizza_id = data.get("pizza_id")
        restaurant_id = data.get("restaurant_id")
        

        pizza = Pizza.query.filter_by(id=pizza_id).first()
        restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
        
        if not (pizza and restaurant):
            return jsonify({'errors': ['Pizza or restaurant not found']}), 404
        
        if not 1 <= price <= 30:
            return jsonify({'errors': ['validation errors']}), 400

        new_restaurant_pizza = RestaurantPizza(
            price=price,
            pizza_id=pizza_id,
            restaurant_id=restaurant_id
        )
        
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        
        response_data = {
            "id": new_restaurant_pizza.id,
            "price": new_restaurant_pizza.price,
            "pizza": {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            },
            "pizza_id": pizza_id,
            "restaurant": {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address
            },
            "restaurant_id": restaurant_id
        }
        
        return jsonify(response_data), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)