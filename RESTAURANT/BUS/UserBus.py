from RESTAURANT.DAO import UserDao as user

def check_login(id, pw):
    account = {
        'employee_id': id,
        'password': pw
    }
    return user.check_login(account)