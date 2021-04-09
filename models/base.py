from database import db


class Model:
    def save(self):
        db.session.add(self)
        db.session.commit()
        print(f"{self} created")

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        print(f"{self} deleted")

    @classmethod
    def find(cls, by=None):
        if by is None:
            return db.session.query(cls).all()
        return db.session.query(cls).filter(by).first()
