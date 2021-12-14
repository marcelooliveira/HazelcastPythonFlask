import sys
from flask import render_template, request, redirect
from ECommerceData import ECommerceData
from app import app

this = sys.modules[__name__]
this.CartItems = None

eCommerceData = ECommerceData()
eCommerceData.Initialize()

@app.route("/payment", methods=['GET', 'POST'])
def payment():
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
      "OrdersAwaitingPayment": this.OrdersAwaitingPayment
    }
    return render_template('payment.html', Model = model)

def InitializePage():
  this.OrdersAwaitingPayment = eCommerceData.OrdersAwaitingPayment()
