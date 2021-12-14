import decimal
from datetime import datetime
from models.BaseEntity import BaseEntity

class Order(BaseEntity):
    def __init__(self, id: int, placement: datetime, itemCount: int, total: decimal, *args, **kwargs):
        self.Placement = placement
        self.ItemCount = itemCount
        self.Total = total
        super(Order, self).__init__(id, *args, **kwargs)



