from sqlalchemy.exc import IntegrityError
from database import db
from models.books import Book, Author, Category, Issues, Publisher
from models.users import User
from datetime import date, timedelta
from utils.hash import hash256
from utils.random_string import generate_random_string
from utils.display import clear_screen, display_list, crud_menu
from utils.db import delete
from utils.input import date_input, multiline_input
from exceptions.issue import FineCheckError, InIssuingError


db.init()

clear_screen()
print("Library Management System")
username = input("Username: ")
password = input("Password: ")
user = User.find(by=User.username == username)
while not user or user.password != hash256(password) or not user.is_librarian:
    print("Username not exist or wrong password or not a librarian")
    username = input("Username: ")
    password = input("Password: ")
    user = User.find(by=User.username == username)

while True:
    clear_screen()
    print("1. Handle users")
    print("2. Handle books")
    print("3. Handle categories")
    print("4. Handle publishers")
    print("5. Handle authors")
    print("6. Handle issues")
    selection = int(input("Selection: "))
    while selection < 1 or selection > 7:
        selection = int(input("Selection: "))

    if selection == 1:
        selection = crud_menu(of="user")
        clear_screen()
        if selection == 1:
            name = input("Name: ")
            card_number = input("Card Number: ")
            while len(card_number) != 14:
                card_number = input("Card Number: ")
            username = card_number
            password = generate_random_string()
            birthday = date_input("Birthday (yyyy-mm-dd): ")
            try:
                User(name=name, username=username, password=hash256(password),
                     birthday=birthday, card_number=card_number).save()
            except IntegrityError as e:
                print("Username or Card Number is duplicated")
        elif selection == 2:
            display_list(of=User)
        else:
            delete(what=User, by=User.id == int(input("User ID: ")))
    elif selection == 2:
        selection = crud_menu("book")
        clear_screen()
        if selection == 1:
            name = input("Name: ")
            authors = []
            while True:
                try:
                    author_id = int(input("Author ID: "))
                    authors.append(Author.find(by=Author.id == author_id))
                    more = input("Continue? (y/n) ")
                    while more != "y" and more != "n":
                        more = input("Continue? (y/n) ")
                    if more == "n":
                        break
                except ValueError:
                    break
            categories = []
            while True:
                try:
                    category_id = int(input("Category ID: "))
                    categories.append(Category.find(
                        by=Category.id == category_id))
                    more = input("Continue? (y/n) ")
                    while more != "y" and more != "n":
                        more = input("Continue? (y/n) ")
                    if more == "n":
                        break
                except ValueError:
                    break
            while True:
                try:
                    publisher_id = int(input("Publisher ID: "))
                    publisher = Publisher.find(by=Publisher.id == publisher_id)
                    break
                except ValueError:
                    continue
            published_date = date_input("Published Date (yyyy-mm-dd): ")
            Book(name=name, published_date=published_date, authors=authors,
                 categories=categories, publisher=publisher).save()
        elif selection == 2:
            display_list(of=Book)
        else:
            delete(what=Book, by=Book.id == int(input("Book ID: ")))
    elif selection == 3:
        selection = crud_menu("category")
        clear_screen()
        if selection == 1:
            name = input("Name: ")
            try:
                Category(name=name).save()
            except IntegrityError:
                print(f"{name} exists")
        elif selection == 2:
            display_list(of=Category)
        elif selection == 3:
            delete(what=Category, by=Category.id ==
                   int(input("Category ID: ")))
    elif selection == 4:
        selection = crud_menu("publisher")
        clear_screen()
        if selection == 1:
            name = input("Name: ")
            founded_date = date_input("Founded Date (yyyy-mm-dd): ")
            description = multiline_input("Description: ")
            Publisher(name=name, founded_date=founded_date,
                      description=description).save()
        elif selection == 2:
            display_list(of=Publisher)
        else:
            delete(what=Publisher, by=Publisher.id ==
                   int(input("Publisher ID: ")))
    elif selection == 5:
        selection = crud_menu("author")
        clear_screen()
        if selection == 1:
            name = input("Name: ")
            gender = input("Gender (M/F): ")
            while gender != "M" and gender != "F":
                gender = input("Gender (M/F): ")
            birthday = date_input("Birthday (yyyy-mm-dd): ")
            nickname = input("Nickname: ")
            Author(name=name, gender=gender,
                   birthday=birthday, nickname=nickname).save()
        elif selection == 2:
            display_list(of=Author)
        else:
            delete(what=Author, by=Author.id == int(input("Author ID: ")))
    elif selection == 6:
        clear_screen()
        print("1. Create an issue")
        print("2. List all issues")
        print("3. Close an issue")
        print("4. Delete an issue")
        selection = int(input("Selection: "))
        while selection < 1 or selection > 4:
            selection = int(input("Selection: "))

        clear_screen()
        if selection == 1:
            while True:
                try:
                    user = User.find(by=User.id == int(input("User ID: ")))
                    break
                except ValueError:
                    continue
            books = []
            issue_count = 0
            while True:
                print(f"Issue count: {issue_count}, Maximum of issues: 3")
                try:
                    if issue_count <= 3:
                        book = Book.find(by=Book.id == int(input("Book ID: ")))
                        books.append(book)
                        issue_count += 1
                        more = input("Continue? (y/n) ")
                        while more != "y" and more != "n":
                            more = input("Continue? (y/n) ")
                        if more == "n":
                            break
                    else:
                        print("Maximum reached")
                        break
                except ValueError:
                    continue
            try:
                for book in books:
                    user.issues(book, start_date=date.today(),
                                end_date=date.today() + timedelta(5))
            except InIssuingError:
                print("Book already in issue")
            except FineCheckError:
                print("User did not pay the fine check")
        elif selection == 2:
            display_list(of=Issues)
        elif selection == 3:
            clear_screen()
            print("1. Return books")
            print("2. Pay fine checks")
            selection = int(input("Selection: "))
            while selection < 1 or selection > 2:
                selection = int(input("Selection: "))

            clear_screen()
            if selection == 1:
                while True:
                    try:
                        user = User.find(by=User.id == int(input("User ID: ")))
                        break
                    except ValueError:
                        continue
                while True:
                    try:
                        book = Book.find(by=Book.id == int(input("Book ID: ")))
                        break
                    except ValueError:
                        continue
                user.returns(book, return_date=date.today())
            else:
                issue = Issues.find(by=Issues.id == int(input("Issue ID: ")))
                while True:
                    try:
                        user = User.find(by=User.id == int(input("User ID: ")))
                        break
                    except ValueError:
                        continue
                user.have_paid_fine_check(of=issue)
        else:
            delete(what=Issues, by=Issues.id == int(input("Issue ID: ")))

    input("Press Enter to continue...")
