from typing import List
from functools import reduce
from datetime import date, datetime
from collections import deque
from BaseECommerceData import IBaseECommerceData, BaseECommerceData
from models.CartItem import CartItem
from models.Order import Order

class IECommerceData(IBaseECommerceData):
    def Initialize():
        pass
    def GetCartItems():
        pass
    def AddCartItem(cartItem: CartItem):
        pass
    def Checkout():
        pass
    def OrdersAwaitingPayment():
        pass
    def OrdersForDelivery():
        pass
    def OrdersRejected():
        pass
    def ApprovePayment():
        pass
    def RejectPayment():
        pass

class ECommerceData(BaseECommerceData): #, IECommerceData
    cartItems = None
    ordersAwaitingPayment = None
    ordersForDelivery = None
    ordersRejected = None

    def Initialize(self):
        self.cartItems = {
            17: CartItem(1, 17, "🥥", "Coconut", 4.50, 2),
            13: CartItem(2, 13, "🍒", "Cherries box", 3.50, 3),
            4: CartItem(3, 4, "🍊", "Tangerine box", 3.50, 1)}

        self.ordersAwaitingPayment = deque([
                Order(1006, datetime(2021, 10, 11, 3, 3, 0), 7, 70.00),
                Order(1007, datetime(2021, 10, 12, 17, 17, 0), 2, 20.00),
                Order(1008, datetime(2021, 10, 13, 21, 9, 0), 5, 50.00)
            ])

        self.ordersForDelivery = deque([
                Order(1002, datetime(2021, 10, 2, 23, 3, 0), 5, 50.00),
                Order(1003, datetime(2021, 10, 9, 7, 7, 0), 3, 30.00)
            ])

        self.ordersRejected = deque([
                Order(1001, datetime(2021, 10, 1, 18, 32, 0), 5, 35.00),
                Order(1004, datetime(2021, 10, 3, 17, 17, 0), 2, 24.00),
                Order(1005, datetime(2021, 10, 7, 9, 12, 0), 4, 17.00)
            ])

        self.MaxOrderId = 1008

    def GetCartItems(self):
        # self.cartItems.sort(key= lambda x:x[0])
        # return self.cartItems.OrderBy(i => i.Key).Select(i => i.Value).ToList()
        return self.cartItems    

    def AddCartItem(self, cartItem: CartItem):
        products = self.GetProductList()
        product = next(filter(lambda p: p.Id == cartItem.ProductId, products), None)
        newItem = CartItem(cartItem.Id, product.Id, product.Icon, product.Description, product.UnitPrice, cartItem.Quantity)
        self.cartItems[newItem.ProductId] = newItem
    
    def OrdersAwaitingPayment(self):
        new_list = list(self.ordersAwaitingPayment)
        new_list.sort(reverse=True, key=lambda o: o.Id)
        return new_list

    def OrdersForDelivery(self):
        return self.ordersForDelivery

    def OrdersRejected(self):
        return self.ordersRejected

    def ApprovePayment(self):
        order = self.ordersAwaitingPayment.popleft()
        self.ordersForDelivery.append(order)

    def RejectPayment(self):
        order = self.ordersAwaitingPayment.popleft()
        self.ordersRejected.append(order)

    def Checkout(self):
        self.MaxOrderId = self.MaxOrderId + 1
        orderId = self.MaxOrderId
        total = sum(map(lambda i: i.Quantity * i.UnitPrice, self.cartItems.values()))
        order = Order(orderId, datetime.now(), len(self.cartItems), total)
        self.ordersAwaitingPayment.append(order)
        self.cartItems.clear()