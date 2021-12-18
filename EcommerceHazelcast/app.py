import atexit
from flask import Flask
from ECommerceDataHazelcast import ECommerceDataHazelcast

app = Flask(__name__)

ecommerce_data = ECommerceDataHazelcast()
ecommerce_data.initialize()

from routes.index import index
from routes.add_to_cart import add_to_cart
from routes.payment import payment
from routes.tracking import tracking

@atexit.register
def exit():
  ecommerce_data.shutdown()