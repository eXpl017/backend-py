import bcrypt

def hash_passwd(passwd: str) -> str:
    passwd_bytes = passwd.encode()
    salt = bcrypt.gensalt()
    hashed_passwd = bcrypt.hashpw(passwd_bytes, salt)
    return str(hashed_passwd)

def verfiy_passwd(login_passwd: str, hashed_passwd: str) -> bool:
    login_passwd_bytes = login_passwd.encode()
    return bcrypt.checkpw()

