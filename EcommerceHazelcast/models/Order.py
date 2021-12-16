class Order():
    def __init__(self, id, placement, item_count, total):
        self.id = id
        self.placement = placement
        self.item_count = item_count
        self.total = total

    def __repr__(self):
        return "Order(id=%s, placement=%s, item_count=%s, total=%s)" % (self.id, self.placement, self.item_count, self.total)
