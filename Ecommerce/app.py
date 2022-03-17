import sys
from flask import Flask

app = Flask(__name__)

from routes.index import index
from routes.add_to_cart import add_to_cart
from routes.payment import payment
from routes.tracking import tracking
