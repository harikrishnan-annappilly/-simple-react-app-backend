from db import db

class ItemModel(db.Model):

    __tablename__ = 'item_tbl'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def find_by_name(cls, name):
        item = cls.query.filter_by(name=name).first()
        return item
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    