from db import db


class MovieModel(db.Model):

    __tablename__ = 'movie_tbl'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    numberInStock = db.Column(db.Integer, nullable=False)
    dailyRentalRate = db.Column(db.Float(precision=2), nullable=False)
    liked = db.Column(db.Boolean, default=False, nullable=False)
    # genre_id = db.Column(db.Integer)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre_tbl.id'))

    def json(self):
        return {
            '_id': self.id,
            'title': self.title,
            'genre': {'_id': self.genre.id, 'name': self.genre.name, },
            'numberInStock': self.numberInStock,
            'dailyRentalRate': self.dailyRentalRate,
            'liked': self.liked,
        }

    def save(self):
        print('going to save')
        db.session.add(self)
        print('added ')
        db.session.commit()
        print('commited')

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_title(cls, title):
        movie = cls.query.filter_by(title=title).first()
        return movie

    @classmethod
    def find_by_id(cls, id):
        movie = cls.query.filter_by(id=id).first()
        return movie

    @classmethod
    def find_all(cls):
        return cls.query.all()


# {
#     _id: "5b21ca3eeb7f6fbccd471815",
#     title: "Terminator",
#     genre: {_id: "5b21ca3eeb7f6fbccd471818", name: "Action"},
#     numberInStock: 6,
#     dailyRentalRate: 2.5,
#     publishDate: "2018-01-03T19:04:28.809Z",
#     liked: true,
# },
