from enum import Enum
class Gender(Enum):
    MALE = 1,
    FEMALE = 2

class Role(Enum):
    ADMIN = 'ADMIN',
    BILLING_STAFF = 'BILLING_STAFF',
    RECEPTIONIST = 'RECEPTIONIST'
class TypeItem(Enum):
    FOOD = 'FOOD',
    DRINK = 'DRINK'

class OrderStatus(Enum):
    WAITTING = 'WAITTING',
    CONFIRMED = 'CONFIRMED',
    CANCLED = 'CANCLED'
    
class Invoice_Status(Enum):
    PENDING = 'PENDING',
    ACCEPTED = 'ACCEPTED'
