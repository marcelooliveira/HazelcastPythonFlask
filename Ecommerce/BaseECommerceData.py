from Singleton import Singleton
from models.Product import Product

class BaseECommerceData(metaclass=Singleton):
    max_order_id = 0

    def get_product_list(self):
        return [Product(1, "🍇", "Grapes box", 3.50),
            Product(2, "🍈", "Melon box", 3.50 ),
            Product(3, "🍉", "Watermelon box", 5.50 ),
            Product(4, "🍊", "Tangerine box", 3.50 ),
            Product(5, "🍋", "Lemon box", 3.50 ),
            Product(6, "🍌", "Banana box", 3.50 ),
            Product(7, "🍍", "Pineapple box", 3.50 ),
            Product(8, "🥭", "Mango box", 4.50 ),
            Product(9, "🍎", "Red Apple box", 3.50 ),
            Product(10, "🍏", "Green Apple box", 6.50 ),
            Product(11, "🍐", "Pear box", 3.50 ),
            Product(12, "🍑", "Peach box", 3.50 ),
            Product(13, "🍒", "Cherries box", 3.50 ),
            Product(14, "🍓", "Strawberry box", 3.50 ),
            Product(15, "🥝", "Kiwi Fruit box", 7.50 ),
            Product(16, "🍅", "Tomato box", 2.50 ),
            Product(17, "🥥", "Coconut", 4.50 )]