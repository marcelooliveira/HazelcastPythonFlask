from datetime import datetime

from BaseECommerceData import BaseECommerceData
from GlobalSerializer import GlobalSerializer
from models.CartItem import CartItem
from models.Order import Order
from hazelcast.proxy.reliable_topic import ReliableMessageListener
import hazelcast

class ECommerceData(BaseECommerceData):
    _hazelcast_client = None
    _cart_items_map = None
    _orders_awaiting_payment = None
    _orders_for_delivery = None
    _orders_rejected = None
    _cp_subsystem = None
    
    def start(self):
        self._hazelcast_client = hazelcast.HazelcastClient(global_serializer=GlobalSerializer)

    def shutdown(self):
        print('*** HAZELCAST SHUTDOWN ***')
        self._hazelcast_client.shutdown()

    def initialize(self):
        self.start()
        self.register_listener()
        self._cp_subsystem = self._hazelcast_client.cp_subsystem
        self._cart_items_map = self._hazelcast_client.get_map("distributed-cartitem-map").blocking()
        self._cart_items_map.clear()
        self._cart_items_map.put(17, CartItem(1, 17, "🥥", "Coconut", 4.50, 2))
        self._cart_items_map.put(13, CartItem(2, 13, "🍒", "Cherries box", 3.50, 3))
        self._cart_items_map.put(4, CartItem(3, 4, "🍊", "Tangerine box", 3.50, 1))

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

    def get_cart_items(self):
        items = list(self._cart_items_map.values())
        items.sort(key=lambda i: i.product_id)
        return items

    def add_cart_item(self, cart_item: CartItem):
        products = self.get_product_list()
        product = next(filter(lambda p: p.id == cart_item.product_id, products), None)
        newItem = CartItem(cart_item.id, product.id, product.icon, product.description, product.unit_price, cart_item.quantity)
        self._cart_items_map.put(newItem.product_id, newItem)
    
    def get_orders_awaiting_payment(self):
        orders = list(self._orders_awaiting_payment.iterator())
        orders.sort(reverse=True, key=lambda o: o.id)
        return orders

    def get_orders_for_delivery(self):
        return list(self._orders_for_delivery.iterator())

    def get_orders_rejected(self):
        return list(self._orders_rejected.iterator())

    def approve_payment(self):
        order = self._orders_awaiting_payment.take()
        self._orders_for_delivery.put(order)

    def reject_payment(self):
        order = self._orders_awaiting_payment.take()
        self._orders_rejected.put(order)

    def check_out(self):
        orderId = self.get_next_order_id()
        items = list(self._cart_items_map.values())
        total = sum(map(lambda i: i.quantity * i.unit_price, items))
        message = {
            "orderId" : orderId, 
            "placement" : datetime.now().strftime("%Y-%m-%d, %H:%M:%S"), 
            "item_count" : len(items), 
            "total" : total
        }        
        self.publish_order(message)
        self._cart_items_map.clear()
        
    def get_next_order_id(self):
        atomic_long = self._cp_subsystem.get_atomic_long("orderId").blocking()
        return atomic_long.increment_and_get()
    
    def publish_order(self, message):
        topic = self._hazelcast_client.get_reliable_topic("ordersTopic").blocking()
        topic.publish(message)
    
    def register_listener(self):
        topic = self._hazelcast_client.get_reliable_topic("ordersTopic").blocking()
        topic.add_listener(self.listener_func)
    
    def listener_func(self, topic_message):
        message = topic_message.message
        order = Order(message['orderId'], message['placement'], message['item_count'], message['total'])
        self._orders_awaiting_payment.put(order)

    