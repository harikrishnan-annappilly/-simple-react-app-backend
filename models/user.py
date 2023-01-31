from db import db


class UserModel(db.Model):

    __tablename__ = 'user_tbl'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), default='user')

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'isAdmin': self.role.lower() == 'admin',
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        if user:
            return user
