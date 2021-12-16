class CartItem():
    def __init__(self, id, product_id, icon, description, unit_price, quantity):
        self.id = id
        self.product_id = product_id
        self.icon = icon
        self.description = description
        self.unit_price = unit_price
        self.quantity = quantity
        self.total = self.total()

    def total(self):
        return (self.quantity) * (self.unit_price) 

    def __repr__(self):
        return "CartItem(id=%s, icon=%s, description=%s, unit_price=%s, quantity=%s, total=%s)" % (self.id, self.icon, self.description, self.unit_price, self.quantity, self.total)
