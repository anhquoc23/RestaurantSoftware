from enum import Enum
class Gender(Enum):
    MALE = 1,
    FEMALE = 2

class Role(Enum):
    ADMIN = 1,
    BILLING_STAFF = 2,
    RECEPTIONIST = 3

class TypeItem(Enum):
    FOOD = 1,
    DRINK = 2

class OrderStatus(Enum):
    WAITTING = 1,
    CONFIRMED = 2,
    CANCLED = 3
    
class Invoice_Status(Enum):
    PENDING = 1,
    ACCEPTED = 2