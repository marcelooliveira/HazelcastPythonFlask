import atexit
from flask import Flask
from ECommerceData import ECommerceData

app = Flask(__name__)

ecommerce_data = ECommerceData()
ecommerce_data.initialize()

from routes.index import index
from routes.add_to_cart import add_to_cart
from routes.payment import payment
from routes.tracking import tracking

@atexit.register
def exit():
  ecommerce_data.shutdown()