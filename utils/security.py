from hashlib import sha256


def generate_password_hash(password):
    return sha256(bytes(password, "utf-8")).hexdigest()


def check_password_hash(password_hash, password):
    return generate_password_hash(password) == password_hash
