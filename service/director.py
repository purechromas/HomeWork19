from dao.director import DirectorDAO


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, director):
        self.dao.create(director)

    def update(self, did, director):
        update_director = self.dao.get_one(did)
        update_director.name = director.get('name')
        self.dao.update(update_director)

    def delete(self, did):
        self.dao.delete(did)
