import bcrypt as encrypt

def hashed_password(pw):
    return encrypt.hashpw(pw.encode(), encrypt.gensalt())