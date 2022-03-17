'''This module containst the class product.'''
class Product():
    '''This class represents the product.'''
    def __init__(self, product_id, icon, description, unit_price):
        self.product_id = product_id
        self.icon = icon
        self.description = description
        self.unit_price = unit_price
