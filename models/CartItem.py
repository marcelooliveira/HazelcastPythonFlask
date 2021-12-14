from models.BaseEntity import BaseEntity

class CartItem(BaseEntity):
    def __init__(self, id, productId, icon, description, unitPrice, quantity, *args, **kwargs):
        self.ProductId = productId
        self.Icon = icon
        self.Description = description
        self.UnitPrice = unitPrice
        self.Quantity = quantity
        self.Total = self.Total()
        super(CartItem, self).__init__(id, *args, **kwargs)

    def Total(self):
        return (self.Quantity) * (self.UnitPrice) 
