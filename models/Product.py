from models.BaseEntity import BaseEntity

class Product(BaseEntity):
    def __init__(self, id, icon, description, unitPrice, *args, **kwargs):
        self.Icon = icon
        self.Description = description
        self.UnitPrice = unitPrice
        super(Product, self).__init__(id, *args, **kwargs)

    def Total(self):
        return (self.Quantity) * (self.UnitPrice) 