from abc import ABC

class BaseEntity(ABC):
    def __init__(self, id):
        self.id = id
