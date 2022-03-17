'''This module represents the shopping cart order.'''
class Order():
    '''This class represents the shopping cart order.'''
    def __init__(self, order_id, placement, item_count, total):
        self.order_id = order_id
        self.placement = placement
        self.item_count = item_count
        self.total = total

    def __repr__(self):
        return (f"Order(id={self.order_id}, placement={self.placement},"
                f"item_count={self.item_count}, total={self.total})")
