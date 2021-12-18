import sys
from flask import render_template, request, redirect
from ECommerceDataHazelcast import ECommerceDataHazelcast
from app import app

this = sys.modules[__name__]

ecommerce_data = ECommerceDataHazelcast()

@app.route("/tracking", methods=['GET', 'POST'])
def tracking():
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

def get_page_result():
    initialize_page()
    model = {
      "OrdersForDelivery": this.orders_for_delivery,
      "OrdersRejected": this.orders_rejected
    }
    return render_template('tracking.html', Model = model)

def initialize_page():
  this.orders_for_delivery = ecommerce_data.get_orders_for_delivery()
  this.orders_rejected = ecommerce_data.get_orders_rejected()
