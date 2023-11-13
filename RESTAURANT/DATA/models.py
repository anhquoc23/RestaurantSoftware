
from sqlalchemy import create_engine, DateTime, Table, Column, Integer, \
    String, Enum, Date, Boolean, MetaData, ForeignKey, Text, DECIMAL, and_
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql.functions import user
from RESTAURANT.UTILS import utils as u
from RESTAURANT.DATA.Enum import Invoice_Status
from datetime import date, datetime, timedelta
import uuid, bcrypt

metadata = MetaData()
Base = declarative_base()
data = create_engine('sqlite:///restaurant.sqlite')
Session = sessionmaker(bind=data)
session = Session()

class Employee(Base):
    __tablename__ = 'employee'

    employee_id = Column(String, primary_key=True)
    full_name = Column(String(255), nullable=False)
    gender = Column(Text)
    birthday = Column(Date, nullable=False)
    phone = Column(String(12), nullable=False)
    email = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)

    account = relationship('Account', backref='employee', lazy=True, uselist=False)
    order_tables = relationship('OrderTable', backref='order_table', lazy=True)
    invoices = relationship('Invoice', backref='employee', lazy=True)
    means = relationship('Mean', backref='employee', lazy=True)

    def __init__(self, full_name, gender, birthday, phone, email):
        self.employee_id = uuid.uuid4().hex
        self.full_name = full_name
        self.gender = gender
        self.birthday = birthday
        self.phone = phone
        self.email = email

    def __str__(self):
        return self.employee_id

class Account(Base):
    __tablename__ = 'account'

    account_id = Column(String, primary_key=True)
    password = Column(String(255), nullable=False)
    role = Column(Text)
    employee_id = Column(String(255), ForeignKey('employee.employee_id'))

    def __init__(self, employee_id, password:str, role):
        self.account_id = uuid.uuid4().hex
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.employee_id = employee_id
        self.role = role
    def __str__(self):
        return self.employee_id

class Menu(Base):
    __tablename__ = 'menu'

    menu_id = Column(String, primary_key=True)
    menu_name = Column(String(255), nullable=False)

    menu_items = relationship('MenuItem', backref='menu', lazy=False)

    def __init__(self):
        self.menu_id = uuid.uuid4().hex
    def __str__(self):
        return self.menu_name



MeanItem = Table(
    'mean_item', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('menu_item_id', String, ForeignKey('menu_item.menu_item_id')),
    Column('mean_id', Integer, ForeignKey('mean.mean_id'))
)

class MenuItem(Base):
    __tablename__ = 'menu_item'

    menu_item_id = Column(String, primary_key=True)
    name_item = Column(String(255), nullable=False)
    type_item = Column(Text)
    description = Column(Text, nullable=True)
    image = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    is_active = Column(Boolean, nullable=False)

    menu_id = Column(String, ForeignKey(Menu.menu_id))
    menu_items = relationship('Mean', secondary=MeanItem, back_populates="means")
    def __init__(self):
        self.menu_item_id = uuid.uuid4()

    def __str__(self):
        return self.name_item

class Mean(Base):
    __tablename__ = 'mean'

    mean_id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now(), nullable=False)

    customer_id = Column(String, ForeignKey('customer.customer_id'))
    employee_id = Column(String, ForeignKey(Employee.employee_id))
    
    order_table_id = Column(Integer, ForeignKey('order.order_table_id'))
    
    means = relationship('MenuItem', secondary=MeanItem, back_populates="menu_items")
    invoices = relationship('Invoice', uselist=False, backref='mean', lazy=True)
    
    def __str__(self):
        return self.mean_id


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
        self.customer_id = uuid.uuid4()
    def __str__(self):
        return self.full_name

class Table(Base):
    __tablename__ = 'table'

    table_id = Column(String, primary_key=True)
    table_number = Column(Integer, nullable=False, unique=True)
    
    orders = relationship('OrderTable', backref='table', lazy=True)

    def __init__(self):
        self.table_id = uuid.uuid4()
    def __str__(self):
        return self.table_number

class OrderTable(Base):
    __tablename__ = 'order'

    order_table_id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    status = Column(Text)
    
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
    invoice_status = Column(Text, default=Invoice_Status.PENDING.value)
    
    employee_id = Column(String, ForeignKey(Employee.employee_id))
    customer_id = Column(String, ForeignKey(Customer.customer_id))
    mean_id = Column(Integer, ForeignKey(Mean.mean_id))

    def __str__(self):
        return self.invoice_id

if __name__ == '__main__':
    # Base.metadata.create_all(data)
    # e1 = Employee(full_name='Nguyễn Anh Quốc', gender=Gender.MALE.name, birthday=date(year=2002, month=12, day=24),
    #               phone='0858038081', email='abc@gmail.com')
    #
    # e2 = Employee(full_name='Nguyễn Trung Hiếu', gender=Gender.MALE.name, birthday=date(year=2002, month=11, day=5),
    #               phone='0858038084', email='abc2@gmail.com')
    # e3 = Employee(full_name='Trần Văn Cương', gender=Gender.MALE.name, birthday=date(year=2002, month=2, day=24),
    #               phone='0858038083', email='abc3@gmail.com')
    # session.add_all([e1, e2, e3])
    # session.commit()
    # e1 = session.scalars(select(Employee.employee_id).filter_by(full_name='Nguyễn Anh Quốc')).first()
    # account1 = Account(employee_id=e1, role=Role.ADMIN.name, password='123456')
    # e2 = session.scalars(select(Employee.employee_id).filter_by(full_name='Trần Văn Cương')).first()
    # account2 = Account(employee_id=e2, role=Role.RECEPTIONIST.name, password='123456')
    # e3 = session.scalars(select(Employee.employee_id).filter_by(full_name='Nguyễn Trung Hiếu')).first()
    # account3 = Account(employee_id=e3, role=Role.BILLING_STAFF.ADMIN.name, password='123456')
    # session.add_all([account1, account2, account3])
    # session.commit()
    #<sqlalchemy.orm.session.Session object at 0x00000231DCE68C90>
    account = session.query(Account).first()
    print(account.employee_id)
