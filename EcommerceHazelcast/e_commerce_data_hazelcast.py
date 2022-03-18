'''Wrapper for Hazelcast Client data operations'''
from datetime import datetime

import sys
import threading
import hazelcast
from global_serializer import GlobalSerializer
from models.cart_item import CartItem
from models.order import Order
from models.product import Product

this = sys.modules[__name__]
this.obj = None
this.lock_for_obj = None

class ECommerceDataHazelcast():
    '''Wraps Hazelcast Client data operations'''
    _hazelcast_client = None
    _cart_items = None
    _orders_awaiting_payment = None
    _orders_for_delivery = None
    _orders_rejected = None
    _cp_subsystem = None
    max_order_id = 0
    # Objects shared by threads:

    @staticmethod
    def get_obj():
        """acquire instance via double-checked locking."""
        this.lock_for_obj = threading.Lock()
        if this.obj is None:
            with this.lock_for_obj:
                if this.obj is None:
                    this.obj = ECommerceDataHazelcast()
        return this.obj

    def start(self):
        '''Initializes Hazelcast client'''
        self._hazelcast_client = hazelcast.HazelcastClient(global_serializer=GlobalSerializer)

    def initialize(self):
        '''Initializes CP subsystem, sample maps and queues'''
        self.start()
        self.register_listener()
        self._cp_subsystem = self._hazelcast_client.cp_subsystem
        self._cart_items = self._hazelcast_client.get_map("distributed-cartitem-map").blocking()
        self._cart_items.clear()
        self._cart_items.put(17, CartItem(1, 17, "🥥", "Coconut", 4.50, 2))
        self._cart_items.put(13, CartItem(2, 13, "🍒", "Cherries box", 3.50, 3))
        self._cart_items.put(4, CartItem(3, 4, "🍊", "Tangerine box", 3.50, 1))

        self._orders_awaiting_payment = self._hazelcast_client.get_queue("distributed-payment-queue").blocking()
        self._orders_awaiting_payment.clear()
        self._orders_awaiting_payment.put(
            Order(self.get_next_order_id(), "2021-10-11 03:03:00", 7, 70.00))
        self._orders_awaiting_payment.put(
            Order(self.get_next_order_id(), "2021-10-12 17:17:00", 2, 20.00))
        self._orders_awaiting_payment.put(
            Order(self.get_next_order_id(), "2021-10-13 21:09:00", 5, 50.00))

        self._orders_for_delivery = self._hazelcast_client.get_queue("distributed-delivery-queue").blocking()
        self._orders_for_delivery.clear()
        self._orders_for_delivery.put(
            Order(self.get_next_order_id(), "2021-10-02 23:03:00", 5, 50.00))
        self._orders_for_delivery.put(
            Order(self.get_next_order_id(), "2021-10-09 07:07:00", 3, 30.00))

        self._orders_rejected = self._hazelcast_client.get_queue("distributed-rejected-queue").blocking()
        self._orders_rejected.clear()
        self._orders_rejected.put(
            Order(self.get_next_order_id(), "2021-10-01 18:32:00", 5, 35.00))
        self._orders_rejected.put(
            Order(self.get_next_order_id(), "2021-10-03 17:17:00", 2, 24.00))
        self._orders_rejected.put(
            Order(self.get_next_order_id(), "2021-10-07 09:12:00", 4, 17.00))

    @classmethod
    def get_product_list(cls):
        '''Initializes the e-commerce with sample data'''
        return [Product(1, "🍇", "Grapes box", 3.50),
            Product(2, "🍈", "Melon box", 3.50 ),
            Product(3, "🍉", "Watermelon box", 5.50 ),
            Product(4, "🍊", "Tangerine box", 3.50 ),
            Product(5, "🍋", "Lemon box", 3.50 ),
            Product(6, "🍌", "Banana box", 3.50 ),
            Product(7, "🍍", "Pineapple box", 3.50 ),
            Product(8, "🥭", "Mango box", 4.50 ),
            Product(9, "🍎", "Red Apple box", 3.50 ),
            Product(10, "🍏", "Green Apple box", 6.50 ),
            Product(11, "🍐", "Pear box", 3.50 ),
            Product(12, "🍑", "Peach box", 3.50 ),
            Product(13, "🍒", "Cherries box", 3.50 ),
            Product(14, "🍓", "Strawberry box", 3.50 ),
            Product(15, "🥝", "Kiwi Fruit box", 7.50 ),
            Product(16, "🍅", "Tomato box", 2.50 ),
            Product(17, "🥥", "Coconut", 4.50 )]

    def get_cart_items(self):
        '''Obtain shopping cart items'''
        items = list(self._cart_items.values())
        items.sort(key=lambda i: i.product_id)
        return items

    def add_cart_item(self, cart_item: CartItem):
        '''Add one item to shopping cart'''
        products = self.get_product_list()
        product = next(filter(lambda p: p.product_id == cart_item.product_id, products), None)
        new_item = CartItem(cart_item.cart_item_id, product.product_id, product.icon, product.description, product.unit_price, cart_item.quantity)
        self._cart_items.put(new_item.product_id, new_item)

    def get_orders_awaiting_payment(self):
        '''Obtain orders awaiting payment'''
        orders = list(self._orders_awaiting_payment.iterator())
        orders.sort(reverse=True, key=lambda o: o.order_id)
        return orders

    def get_orders_for_delivery(self):
        '''Obtain orders ready for delivery'''
        return list(self._orders_for_delivery.iterator())

    def get_orders_rejected(self):
        '''Obtain orders with rejected payment'''
        return list(self._orders_rejected.iterator())

    def approve_payment(self):
        '''Move order from awaiting payment to ready for delivery'''
        order = self._orders_awaiting_payment.take()
        self._orders_for_delivery.put(order)

    def reject_payment(self):
        '''Move order from awaiting payment to payment rejected'''
        order = self._orders_awaiting_payment.take()
        self._orders_rejected.put(order)

    def check_out(self):
        '''create a new order and clear the shopping cart'''
        order_id = self.get_next_order_id()
        items = list(self._cart_items.values())
        total = sum(map(lambda i: i.quantity * i.unit_price, items))
        message = {
            "order_id" : order_id,
            "placement" : datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
            "item_count" : len(items),
            "total" : total
        }
        self.publish_order(message)
        self._cart_items.clear()

    def get_next_order_id(self):
        '''obtain the next sequential order id'''
        atomic_long = self._cp_subsystem.get_atomic_long("order_id").blocking()
        return atomic_long.increment_and_get()

    def publish_order(self, message):
        '''publish the order in Hazelcast topic'''
        topic = self._hazelcast_client.get_reliable_topic("new_orders").blocking()
        topic.publish(message)

    def register_listener(self):
        '''register Hazelcast topic'''
        topic = self._hazelcast_client.get_reliable_topic("new_orders").blocking()
        topic.add_listener(self.listener)

    def listener(self, topic_message):
        '''put order awaiting payment in queue'''
        message = topic_message.message
        order = Order(message['order_id'], message['placement'], message['item_count'], message['total'])
        self._orders_awaiting_payment.put(order)
   