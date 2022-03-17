'''This module containst the class product.'''
from models.base_entity import BaseEntity

class Product(BaseEntity):
    '''This class represents the product.'''
    def __init__(self, id, icon, description, unit_price, *args, **kwargs):
        self.icon = icon
        self.description = description
        self.unit_price = unit_price
        super(Product, self).__init__(id, *args, **kwargs)

    def total(self):
        return (self.quantity) * (self.unit_price) 