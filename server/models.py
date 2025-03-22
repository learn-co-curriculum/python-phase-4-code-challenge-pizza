from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
     # add relationship

    pizzas = db.relationship('Pizza', secondary='restaurant_pizza', back_populates='restaurants')

    # add serialization rules
    @validates('price')
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        return price

    def to_dict(self):
        return {
            'restaurant_id': self.restaurant_id,
            'pizza_id': self.pizza_id,
            'price': self.price
        }

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
restaurants = db.relationship('Restaurant', secondary='restaurant_pizza', back_populates='pizzas')
    # add serialization rules
@validates('name')
def validate_name(self, key, name):
        if not name:
            raise ValueError("Pizza name cannot be empty")
        return name
    

def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships
    

    # add serialization rules
    @validates('price')
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        return price

    def to_dict(self):
        return {
            'restaurant_id': self.restaurant_id,
            'pizza_id': self.pizza_id,
            'price': self.price
        }

    # add validation

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
