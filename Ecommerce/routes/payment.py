'''handles requests to the e-commerce payment page'''
import sys
from flask import render_template, request
from e_commerce_data import ECommerceData
from app import app

this = sys.modules[__name__]

ecommerce_data = ECommerceData()
ecommerce_data.initialize()

@app.route("/payment", methods=['GET', 'POST'])
def payment():
    '''handles requests to the e-commerce payment page'''
    if request.method == 'POST':
        return on_post()
    return on_get()

def on_post():
    '''handles post requests to the e-commerce payment page'''
    if 'approveSubmit' in request.form.keys():
        ecommerce_data.approve_payment()
    if 'rejectSubmit' in request.form.keys():
        ecommerce_data.reject_payment()
    return on_get()

def initialize_page():
    '''initializes e-commerce payment page with sample orders'''
    this.orders_awaiting_payment = ecommerce_data.get_orders_awaiting_payment()

def on_get():
    '''handles get requests to the e-commerce payment page'''
    initialize_page()
    model = {
        "OrdersAwaitingPayment": this.orders_awaiting_payment
    }
    return render_template('payment.html', Model = model)
