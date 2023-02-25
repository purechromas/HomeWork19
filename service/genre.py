from dao.genre import GenreDAO


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, gid):
        return self.dao.get_one(gid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, genre):
        self.dao.create(genre)

    def update(self, gid, genre):
        update_genre = self.dao.get_one(gid)
        update_genre.name = genre.get('name')
        self.dao.update(update_genre)

    def delete(self, gid):
        self.dao.delete(gid)
