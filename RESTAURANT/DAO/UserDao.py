from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from RESTAURANT.DATA.models import Employee, Account
import bcrypt
data = create_engine('sqlite:///../DATA/restaurant.sqlite')
Session = sessionmaker(bind=data)
session = Session()

def check_login(account):
    user = session.query(Account).filter(Account.employee_id == account['employee_id']).first()
    if not user is None:
        if bcrypt.checkpw(account['password'].encode(), user.password):
            return True
    return False

if __name__ == '__main__':
    pass