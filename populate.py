from app import app
from db import db

from models.genres import GenreModel
from models.movies import MovieModel

with app.app_context():
    print('populating')
    action = GenreModel(name='Action')
    thriller = GenreModel(name='Thriller')
    comedy = GenreModel(name='Comedy')
    sci_fi = GenreModel(name='Sci-Fi')

    movie1 = MovieModel(title='Avengers', numberInStock=1,
                        dailyRentalRate=10, liked=False, genre=action)
    movie2 = MovieModel(title='Life of pi', numberInStock=1,
                        dailyRentalRate=10, liked=False, genre=action)
    movie3 = MovieModel(title='Hunger Games', numberInStock=1,
                        dailyRentalRate=10, liked=False, genre=action)
    movie4 = MovieModel(title='Dont break', numberInStock=1,
                        dailyRentalRate=10, liked=False, genre=thriller)
    movie5 = MovieModel(title='Sherlock homes', numberInStock=1,
                        dailyRentalRate=10, liked=False, genre=thriller)
    movie6 = MovieModel(title='We are the millers', numberInStock=1,
                        dailyRentalRate=10, liked=False, genre=thriller)
    movie7 = MovieModel(title='Bean', numberInStock=1,
                        dailyRentalRate=10, liked=False, genre=comedy)
    movie8 = MovieModel(title='We are the tuskers', numberInStock=1,
                        dailyRentalRate=10, liked=False, genre=comedy)
    movie9 = MovieModel(title='Passanger', numberInStock=1,
                        dailyRentalRate=10, liked=False, genre=sci_fi)
    movie10 = MovieModel(title='Tenet', numberInStock=1,
                         dailyRentalRate=10, liked=False, genre=sci_fi)
    movie11 = MovieModel(title='Avatar', numberInStock=1,
                         dailyRentalRate=10, liked=False, genre=sci_fi)
    movie12 = MovieModel(title='Interstellar', numberInStock=1,
                         dailyRentalRate=10, liked=False, genre=sci_fi)

    db.session.add_all([action, thriller, comedy, sci_fi])
    db.session.add_all([
        movie1,
        movie2,
        movie3,
        movie4,
        movie5,
        movie6,
        movie7,
        movie8,
        movie9,
        movie10,
        movie11,
        movie12,
    ])
    db.session.commit()

    print('populated')

    # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(40))
    # numberInStock = db.Column(db.Integer, nullable=False)
    # dailyRentalRate = db.Column(db.Float(precision=2), nullable=False)
    # liked = db.Column(db.Boolean, default=False, nullable=False)
    # genre_id = db.Column(db.Integer, db.ForeignKey('genre_tbl.id'))
