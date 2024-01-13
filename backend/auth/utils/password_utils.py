from bcrypt import gensalt, hashpw

def hash_password(password: str) -> str:
    # Generate a salt and hash the password
    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

