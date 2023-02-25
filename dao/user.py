from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def create(self, user):
        new_user = User(**user)
        self.session.add(new_user)
        self.session.commit()

    def update(self, user):
        self.session.add(user)
        self.session.commit()

    def delete(self, uid):
        user = self.session.query(User).get(uid)
        self.session.delete(user)
        self.session.commit()

