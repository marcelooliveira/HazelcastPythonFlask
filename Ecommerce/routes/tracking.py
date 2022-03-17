'''handles requests to the e-commerce order tracking page'''
import sys
from flask import render_template, request
from e_commerce_data import ECommerceData
from app import app

this = sys.modules[__name__]

ecommerce_data = ECommerceData()
ecommerce_data.initialize()

@app.route("/tracking", methods=['GET', 'POST'])
def tracking():
    '''handles requests to the e-commerce order tracking page'''
    if request.method == 'POST':
        return on_post()
    return on_get()

def on_post():
    '''handles post requests to the e-commerce order tracking page'''
    if 'approveSubmit' in request.form.keys():
        ecommerce_data.approve_payment()
    if 'rejectSubmit' in request.form.keys():
        ecommerce_data.reject_payment()
    return on_get()

def on_get():
    '''handles get requests to the e-commerce order tracking page'''
    initialize_page()
    model = {
        "OrdersForDelivery": this.orders_for_delivery,
        "OrdersRejected": this.orders_rejected
    }
    return render_template('tracking.html', Model = model)

def initialize_page():
    '''initializes e-commerce order tracking page with sample orders'''
    this.orders_for_delivery = ecommerce_data.get_orders_for_delivery()
    this.orders_rejected = ecommerce_data.get_orders_rejected()
