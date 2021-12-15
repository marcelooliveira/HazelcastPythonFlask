from models.BaseEntity import BaseEntity

class CartItem(BaseEntity):
    def __init__(self, id, product_id, icon, description, unit_price, quantity, *args, **kwargs):
        self.product_id = product_id
        self.icon = icon
        self.description = description
        self.unit_price = unit_price
        self.quantity = quantity
        self.total = self.total()
        super(CartItem, self).__init__(id, *args, **kwargs)

    def total(self):
        return (self.quantity) * (self.unit_price) 
