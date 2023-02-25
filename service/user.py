import base64
import hashlib
import hmac

from helpers.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS

from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user):
        user['password'] = self.create_hash_password(user.get('password'))
        return self.dao.create(user)

    def update(self, uid, user):
        update_user = self.dao.get_one(uid)

        update_user.username = user.get('username')
        update_user.password = self.create_hash_password(user.get('password'))
        update_user.role = user.get('role')

        return self.dao.update(update_user)

    def update_partial(self, uid, user):
        update_user = self.get_one(uid)

        if 'username' in user:
            update_user.username = user.get('username')
        if 'password' in user:
            update_user.password = self.create_hash_password(user.get('password'))
        if 'role' in user:
            update_user.role = user.get('role')

        return self.dao.update(update_user)

    def delete(self, uid):
        return self.dao.delete(uid)

    def create_hash_password(self, password):
        encode_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(encode_digest)

    def compare_password(self, db_password, other_password) -> bool:
        encode_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        decode_digest = base64.b64decode(db_password)

        return hmac.compare_digest(decode_digest, encode_digest)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)
