from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    and_,
    or_
)
from sqlalchemy.orm import relationship
from database import db
from .base import Model
from .books import Issues
from exceptions.issue import InIssuingError, FineCheckError


class User(db.Base, Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    username = Column(String(16), unique=True)
    password = Column(String(16))
    birthday = Column(Date)
    card_number = Column(String(14), unique=True)
    is_librarian = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    books = relationship("Book", secondary="issues", back_populates="users")

    def __repr__(self):
        return f"<User(name={self.name}, birthday={self.birthday})>"

    def issues(self, book, start_date, end_date):
        if db.session.query(Issues) \
            .filter(
                and_(
                    Issues.book_id == book.id,
                    or_(Issues.return_date == None,
                        and_(Issues.return_date > Issues.end_date,
                             Issues.did_pay_fine_check == False)
                        ))).first():
            raise InIssuingError()

        issue = Issues(book_id=book.id, user_id=self.id,
                       start_date=start_date, end_date=end_date)
        issue.save()

    def returns(self, book, return_date):
        issue = db.session.query(Issues).filter(
            and_(Issues.book_id == book.id, Issues.return_date == None)).first()
        issue.return_date = return_date
        issue.did_pay_fine_check = None if return_date == issue.end_date else False
        db.session.add(issue)
        db.session.commit()

    def have_paid_fine_check(self, of):
        of.did_pay_fine_check = True
        db.session.add(of)
        db.session.commit()
