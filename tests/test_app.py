from database import db
from models.books import Author, Book, Category, Publisher, User
from datetime import date
import pytest


@pytest.fixture(scope="session", autouse=True)
def init(request):
    db.init()
    Author(name="Tara Westover", gender="F", birthday=date(1983, 12, 1)).save()
    [category.save()
     for category in [Category(name="biography"), Category("autography")]]
    Publisher(name="O'Really", founded_date=date(1960, 2, 2)).save()


def test_create_a_user():
    user = User(name="a", birthday=date(1999, 11, 2),
                card_number="123456789012345")
    user.save()
    assert type(user.id) == int


def test_create_a_book():
    book = Book(
        name="Educated",
        published_date=date(2018, 1, 1),
        authors=[Author()],
        categories=[Category()],
        publisher=Publisher()
    )
