import decimal
from datetime import datetime
from models.BaseEntity import BaseEntity

class Order(BaseEntity):
    def __init__(self, id: int, placement: datetime, item_count: int, total: decimal, *args, **kwargs):
        self.placement = placement
        self.item_count = item_count
        self.total = total
        super(Order, self).__init__(id, *args, **kwargs)



