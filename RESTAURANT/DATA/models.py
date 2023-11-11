import uuid

from sqlalchemy import create_engine, DateTime, Table, Column, Integer, \
    String, Enum, Date, Boolean, MetaData, ForeignKey, UUID, Text, DECIMAL
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from Enum import Gender, Role, TypeItem, OrderStatus, Invoice_Status
from datetime import date, datetime, timedelta
import uuid

metadata = MetaData()
Base = declarative_base()
data = create_engine('sqlite:///restaurant.sqlite')


class Employee(Base):
    __tablename__ = 'employee'

    employee_id = Column(String, primary_key=True)
    full_name = Column(String(255), nullable=False)
    gender = Column(Enum(Gender))
    birthday = Column(Date, nullable=False)
    phone = Column(String(12), nullable=False)
    email = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)

    account = relationship('Account', backref='employee', lazy=True, uselist=False)
    order_tables = relationship('OrderTable', backref='order_table', lazy=True)
    invoices = relationship('Invoice', backref='employee', lazy=True)
    means = relationship('Mean', backref='employee', lazy=True)

    def __init__(self):
        self.employee_id = uuid.uuid5().hex

    def __str__(self):
        return self.employee_id

class Account(Base):
    __tablename__ = 'account'

    account_id = Column(String, primary_key=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(Role))
    employee_id = Column(String(255), ForeignKey('employee.employee_id'))

    def __init__(self):
        self.account_id = uuid.uuid5().hex
    def __str__(self):
        return self.employee_id

class Menu(Base):
    __tablename__ = 'menu'

    menu_id = Column(String, primary_key=True)
    menu_name = Column(String(255), nullable=False)

    menu_items = relationship('MenuItem', backref='menu', lazy=False)

    def __init__(self):
        self.menu_id = uuid.uuid5().hex
    def __str__(self):
        return self.menu_name


class MenuItem(Base):
    __tablename__ = 'menu_item'

    menu_item_id = Column(String, primary_key=True)
    name_item = Column(String(255), nullable=False)
    type_item = Column(Enum(TypeItem))
    description = Column(Text, nullable=True)
    image = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    is_active = Column(Boolean, nullable=False)

    menu_id = Column(String, ForeignKey(Menu.menu_id))
    menu_item_mean_id = relationship('MeanItem', secondary='mean_item', back_populates='mean_items')

    def __init__(self):
        self.menu_item_id = uuid.uuid5()

    def __str__(self):
        return self.name_item

class Mean(Base):
    __tablename__ = 'mean'

    mean_id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now(), nullable=False)

    customer_id = Column(String, ForeignKey('customer.customer_id'))
    employee_id = Column(String, ForeignKey(Employee.employee_id))
    
    order_table_id = Column(Integer, ForeignKey('order.order_table_id'))
    
    mean_items = relationship('MenuItem', secondary='mean_item', back_populates='means')
    invoices = relationship('Invoice', uselist=False, backref='mean', lazy=True)
    
    def __str__(self):
        return self.mean_id
    
    
    

MeanItem = Table('mean_item', Base.metadata,
                 Column('mean_item_id', Integer, primary_key=True, autoincrement=True),
                 Column('mean_id', Integer, ForeignKey(Mean.mean_id)),
                 Column('item_id', String, ForeignKey(MenuItem.menu_item_id)))

class Customer(Base):
    __tablename__ = 'customer'

    customer_id = Column(String, primary_key=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(12), nullable=False)
    email = Column(String, nullable=False)
    
    means = relationship('Mean', backref='customer', lazy=True)
    orders = relationship('OrderTable', backref='customer', lazy=True)
    invoices = relationship('Invoice', backref='customer', lazy=True)

    def __init__(self):
        self.customer_id = uuid.uuid5()
    def __str__(self):
        return self.full_name

class Table(Base):
    __tablename__ = 'table'

    table_id = Column(String, primary_key=True)
    table_number = Column(Integer, nullable=False, unique=True)
    
    orders = relationship('OrderTable', backref='table', lazy=True)

    def __init__(self):
        self.table_id = uuid.uuid5()
    def __str__(self):
        return self.table_number

class OrderTable(Base):
    __tablename__ = 'order'

    order_table_id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    status = Column(Enum(OrderStatus))
    
    employee_id = Column(String, ForeignKey(Employee.employee_id))
    customer_id = Column(String, ForeignKey(Customer.customer_id))
    table_id = Column(String, ForeignKey(Table.table_id))
    
    mean = relationship('Mean', uselist=False, backref='order_table', lazy=True)

    def __str__(self):
        return self.order_table_id
    
class Invoice(Base):
    __tablename__ = 'invoice'
    
    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    invoice_status = Column(Enum(Invoice_Status), default=Invoice_Status.PENDING)
    
    employee_id = Column(String, ForeignKey(Employee.employee_id))
    customer_id = Column(String, ForeignKey(Customer.customer_id))
    mean_id = Column(Integer, ForeignKey(Mean.mean_id))
    
    def __str__(self):
        return self.invoice_id

if __name__ == '__main__':
    try:
        Base.metadata.create_all(data)
        print('Start File Restaurant.sqlite Success')
    except:
        print('Error When Start Restaurant.sqlite')