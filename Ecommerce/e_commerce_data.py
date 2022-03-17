'''Wrapper for Hazelcast Client data operations'''
from datetime import datetime
from collections import deque
from base_e_commerce_data import BaseECommerceData
from models.cart_item import CartItem
from models.order import Order

class ECommerceData(BaseECommerceData):
    '''Wraps Hazelcast Client data operations'''
    _cart_items = None
    _orders_awaiting_payment = None
    _orders_for_delivery = None
    _orders_rejected = None

    def initialize(self):
        '''Initializes CP subsystem, sample maps and queues'''
        self._cart_items = {
            17: CartItem(1, 17, "🥥", "Coconut", 4.50, 2),
            13: CartItem(2, 13, "🍒", "Cherries box", 3.50, 3),
            4: CartItem(3, 4, "🍊", "Tangerine box", 3.50, 1)}

        self._orders_awaiting_payment = deque([
                Order(1006, datetime(2021, 10, 11, 3, 3, 0), 7, 70.00),
                Order(1007, datetime(2021, 10, 12, 17, 17, 0), 2, 20.00),
                Order(1008, datetime(2021, 10, 13, 21, 9, 0), 5, 50.00)
            ])

        self._orders_for_delivery = deque([
                Order(1002, datetime(2021, 10, 2, 23, 3, 0), 5, 50.00),
                Order(1003, datetime(2021, 10, 9, 7, 7, 0), 3, 30.00)
            ])

        self._orders_rejected = deque([
                Order(1001, datetime(2021, 10, 1, 18, 32, 0), 5, 35.00),
                Order(1004, datetime(2021, 10, 3, 17, 17, 0), 2, 24.00),
                Order(1005, datetime(2021, 10, 7, 9, 12, 0), 4, 17.00)
            ])

        self._max_order_id = 1008

    def get_cart_items(self):
        items = list(self._cart_items.values())
        items.sort(key=lambda i: i.product_id)
        return items    

    def add_cart_item(self, cart_item: CartItem):
        '''Add one item to shopping cart'''
        products = self.get_product_list()
        product = next(filter(lambda p: p.id == cart_item.product_id, products), None)
        new_item = CartItem(cart_item.id, product.id, product.icon, product.description, product.unit_price, cart_item.quantity)
        self._cart_items[new_item.product_id] = new_item

    def get_orders_awaiting_payment(self):
        '''Obtain orders awaiting payment'''
        orders = list(self._orders_awaiting_payment)
        orders.sort(reverse=True, key=lambda o: o.id)
        return orders

    def get_orders_for_delivery(self):
        '''Obtain orders ready for delivery'''
        return self._orders_for_delivery

    def get_orders_rejected(self):
        '''Obtain orders with rejected payment'''
        return self._orders_rejected

    def approve_payment(self):
        '''Move order from awaiting payment to ready for delivery'''
        order = self._orders_awaiting_payment.popleft()
        self._orders_for_delivery.append(order)

    def reject_payment(self):
        '''Move order from awaiting payment to payment rejected'''
        order = self._orders_awaiting_payment.popleft()
        self._orders_rejected.append(order)

    def check_out(self):
        '''create a new order and clear the shopping cart'''
        self._max_order_id = self._max_order_id + 1
        order_id = self._max_order_id
        total = sum(map(lambda i: i.quantity * i.unit_price, self._cart_items.values()))
        order = Order(order_id, datetime.now(), len(self._cart_items), total)
        self._orders_awaiting_payment.append(order)
        self._cart_items.clear()