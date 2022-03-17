'''This module represents a group of a specific product in the cart.'''
from models.base_entity import BaseEntity

class CartItem(BaseEntity):
    '''This class represents a group of a specific product in the cart.'''
    def __init__(self, id, product_id, icon, description, unit_price, quantity, *args, **kwargs):
        self.product_id = product_id
        self.icon = icon
        self.description = description
        self.unit_price = unit_price
        self.quantity = quantity
        self.total = self.total()
        super(CartItem, self).__init__(id, *args, **kwargs)

    def total(self):
        '''gets the total amount for the cart item'''
        return (self.quantity) * (self.unit_price) 
