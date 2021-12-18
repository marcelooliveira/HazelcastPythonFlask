import sys
from flask import render_template, request, redirect
from ECommerceDataHazelcast import ECommerceDataHazelcast
from app import app

this = sys.modules[__name__]

ecommerce_data = ECommerceDataHazelcast()

@app.route("/payment", methods=['GET', 'POST'])
def payment():
    if request.method == 'GET':
      return on_get()
    elif request.method == 'POST':
      return on_post()

def on_get():
    return get_page_result()

def on_post():
    if 'approveSubmit' in request.form.keys():
      ecommerce_data.approve_payment()
    if 'rejectSubmit' in request.form.keys():
      ecommerce_data.reject_payment()
    return get_page_result()

def initialize_page():
  this.orders_awaiting_payment = ecommerce_data.get_orders_awaiting_payment()

def get_page_result():
    initialize_page()
    model = {
      "OrdersAwaitingPayment": this.orders_awaiting_payment
    }
    return render_template('payment.html', Model = model)
