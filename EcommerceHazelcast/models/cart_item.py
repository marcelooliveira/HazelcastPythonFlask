'''This module represents a group of a specific product in the cart.'''
class CartItem():
    '''This class represents a group of a specific product in the cart.'''
    def __init__(self, cart_item_id, product_id, icon, description, unit_price, quantity):
        self.cart_item_id = cart_item_id
        self.product_id = product_id
        self.icon = icon
        self.description = description
        self.unit_price = unit_price
        self.quantity = quantity
        self.total = self.get_total()

    def get_total(self):
        '''gets the total amount for the cart item'''
        return (self.quantity) * (self.unit_price)

    def __repr__(self):
        return (f"CartItem(id={self.cart_item_id}, icon={self.icon}," 
                f"description={self.description}, unit_price={self.unit_price},"
                f"quantity={self.quantity}, total={self.get_total})")
