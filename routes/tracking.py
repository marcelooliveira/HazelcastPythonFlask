import sys
from flask import render_template, request, redirect
from ECommerceData import ECommerceData
from app import app

this = sys.modules[__name__]
this.CartItems = None

eCommerceData = ECommerceData()
eCommerceData.Initialize()

@app.route("/tracking", methods=['GET', 'POST'])
def tracking():
    if request.method == 'GET':
      return OnGet()
    elif request.method == 'POST':
      return OnPost()

def OnGet():
    return get_page_result()

def OnPost():
    if 'approveSubmit' in request.form.keys():
      eCommerceData.ApprovePayment()
    if 'rejectSubmit' in request.form.keys():
      eCommerceData.RejectPayment()
    return get_page_result()

def get_page_result():
    InitializePage()
    model = {
      "OrdersForDelivery": this.OrdersForDelivery,
      "OrdersRejected": this.OrdersRejected
    }
    return render_template('tracking.html', Model = model)

def InitializePage():
  this.OrdersForDelivery = eCommerceData.OrdersForDelivery()
  this.OrdersRejected = eCommerceData.OrdersRejected()
