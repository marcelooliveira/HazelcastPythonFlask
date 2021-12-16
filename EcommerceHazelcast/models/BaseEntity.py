from hazelcast.serialization.api import IdentifiedDataSerializable
from abc import ABC

class BaseEntity(ABC):
    FACTORY_ID = 1;
    EMPLOYEE_TYPE = 1;
        
    def __init__(self, id):
        self.id = id
    

