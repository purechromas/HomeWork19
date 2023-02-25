from dao.model.director import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Director).get(bid)

    def get_all(self):
        return self.session.query(Director).all()

    def create(self, director):
        ent = Director(**director)
        self.session.add(ent)
        self.session.commit()

    def update(self, director):
        self.session.add(director)
        self.session.commit()

    def delete(self, did):
        director = self.get_one(did)
        self.session.delete(director)
        self.session.commit()
