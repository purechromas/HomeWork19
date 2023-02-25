import calendar
import datetime
import jwt
from flask import abort

from helpers.constants import JWT_ALGORITHM, JWT_SECRET
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_token(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not self.user_service.compare_password(user.password, password):
                abort(400)

        data = {
            'username': user.username,
            'role': user.role
        }

        # access token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['expire'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # refresh token
        day = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        data['expire'] = calendar.timegm(day.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = data.get('username')

        user = self.user_service.get_by_username(username=username)

        if user is None:
            abort(404)
        return self.generate_token(username, user.password, is_refresh=True)
