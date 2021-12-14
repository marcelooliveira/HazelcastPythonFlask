import sys
from flask import Flask, render_template, request, redirect
from ECommerceData import ECommerceData
from models.CartItem import CartItem

app = Flask(__name__)

from routes.index import index
from routes.addToCart import addToCart
from routes.payment import payment
from routes.tracking import tracking

