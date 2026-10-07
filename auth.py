import bcrypt
from database import user_exists, save_user, get_user
from crypto_utils import generate_salt, derive_key


def hash_master_password(master_password):
    return bcrypt.hashpw(
        master_password.encode(),
        bcrypt.gensalt()
    )


def verify_master_password(master_password, stored_hash):
    return bcrypt.checkpw(
        master_password.encode(),
        stored_hash
    )


def register_master_password(master_password):
    salt = generate_salt()
    master_hash = hash_master_password(master_password)
    save_user(master_hash, salt)
    return derive_key(master_password, salt)


def login_master_password(master_password):
    if not user_exists():
        return None

    user = get_user()
    stored_hash = user[0]
    salt = user[1]

    if verify_master_password(master_password, stored_hash):
        return derive_key(master_password, salt)

    return None