import sys
from flask import render_template, request, redirect
from ECommerceData import ECommerceData
from app import app

this = sys.modules[__name__]
this.CartItems = None

eCommerceData = ECommerceData()
eCommerceData.Initialize()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
      return OnGet()
    elif request.method == 'POST':
      return OnPost()

def OnGet():
    InitializePage()
    model = {
      "CartItems": this.CartItems
    }
    return render_template('index.html', Model = model)

def OnPost():
    if 'addToCartSubmit' in request.form.keys():
      return redirect('/addToCart')
    if 'checkoutSubmit' in request.form.keys():
      eCommerceData.Checkout()

    model = {
      "CartItems": this.CartItems
    }
    return render_template('index.html', Model = model)

def InitializePage():
  this.CartItems = eCommerceData.GetCartItems()
