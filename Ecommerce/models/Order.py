'''This module represents the shopping cart order.'''
import decimal
from datetime import datetime
from models.base_entity import BaseEntity

'''This module represents the shopping cart order.'''
class Order(BaseEntity):
    '''This class represents the shopping cart order.'''
    def __init__(self, id: int, placement: datetime, item_count: int, total: decimal, *args, **kwargs):
        self.placement = placement
        self.item_count = item_count
        self.total = total
        super(Order, self).__init__(id, *args, **kwargs)



