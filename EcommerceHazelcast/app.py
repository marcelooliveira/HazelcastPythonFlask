'''application entry point'''
from flask import Flask
from e_commerce_data_hazelcast import ECommerceDataHazelcast

app = Flask(__name__)

ecommerce_data = ECommerceDataHazelcast()
ecommerce_data.initialize()

from routes.index import index
from routes.add_to_cart import add_to_cart
from routes.payment import payment
from routes.tracking import tracking
