from click import pass_context
from passlib.context import CryptContext

pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password):
    return pass_context.hash(password)
