from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Text,
    Boolean,
    CheckConstraint,
    ForeignKey
)
from sqlalchemy.orm import relationship
from database import db
from .base import Model


class Has(db.Base, Model):
    __tablename__ = "has"
    author_id = Column(Integer, ForeignKey("author.id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"), primary_key=True)


class Are(db.Base, Model):
    __tablename__ = "are"
    category_id = Column(Integer, ForeignKey("category.id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"), primary_key=True)


class Issues(db.Base, Model):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    start_date = Column(Date)
    end_date = Column(Date, CheckConstraint("end_date >= start_date"))
    return_date = Column(Date, CheckConstraint("return_date >= start_date"))
    did_pay_fine_check = Column(Boolean, nullable=True)

    def __repr__(self):
        return f"<Issue (book_id={self.book_id}, user_id={self.user_id}, start_date={self.start_date}, end_date={self.end_date}, return_date={self.return_date}, did_pay_fine_check={self.did_pay_fine_check})>"


class Book(db.Base, Model):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    published_date = Column(Date)
    publisher_id = Column(Integer, ForeignKey("publisher.id"))

    authors = relationship("Author", secondary="has", back_populates="books")
    categories = relationship(
        "Category", secondary="are", back_populates="books")
    users = relationship("User", secondary="issues", back_populates="books")
    publisher = relationship("Publisher", back_populates="books")

    def __repr__(self):
        return f"<Book(name={self.name}, publised_date={self.published_date})>"


class Category(db.Base, Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True)

    books = relationship("Book", secondary="are", back_populates="categories")

    def __repr__(self):
        return f"<Category(name={self.name})>"


class Publisher(db.Base, Model):
    __tablename__ = "publisher"
    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    founded_date = Column(Date)
    description = Column(Text, nullable=True)

    books = relationship("Book", order_by=Book.id, back_populates="publisher")

    def __repr__(self):
        return f"<Category(name={self.name}, founded_date={self.founded_date})>"


class Author(db.Base, Model):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    gender = Column(String(1), CheckConstraint("gender = 'M' OR gender = 'F'"))
    birthday = Column(Date)
    nickname = Column(String(25), nullable=True)

    books = relationship("Book", secondary="has", back_populates="authors")

    def __repr__(self):
        return f"<Author(name={self.name}, gender={self.gender}, birthday={self.birthday}, nickname={self.nickname})>"
