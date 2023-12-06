from main import db
from flask import Blueprint
# from main import bcrypt
from models.users import User
from models.threads import Thread
from datetime import date

db_commands = Blueprint("db", __name__)

@db_commands .cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands .cli.command("seed")
def seed_db():

    # Admin user
    admin_user = User(
        name = "Admin",
        email = "admin@cramhub.com",
        cohort = "Admin Team",
        admin = True
    )
    db.session.add(admin_user)

    # User 1
    user1 = User(
        name = "Ayrton Senna",
        email = "senna@gmail.com",
        cohort = "2023 September Accelerated",
    )
    db.session.add(user1)
    
    # User 2
    user2 = User(
        name = "Harry Potter",
        email = "xXhazza_pXx@owlmail.com",
        cohort = "2022 May Standard",
    )
    db.session.add(user2)

    # Thread 1
    thread1 = Thread(
        category = "HTML",
        title = "HTML Basics",
        date = date.today(),
        description = "Good introduction to HTML5 that really helped me understand the basics of what HTML is and what we can do with it",
        link = "https://www.youtube.com/watch?v=8_YadxRXGaA"
    )
    db.session.add(thread1)

    # Thread 2
    thread2 = Thread(
        category = "CSS",
        title = "Cool animations with CSS",
        date = date.today(),
        description = "Found this website that has a list of cool animations you can do with CSS. Will be adding some of these to my portfolio",
        link = "https://www.w3schools.com/css/css3_animations.asp"
    )
    db.session.add(thread2)

    # Thread 3
    thread3 = Thread(
        category = "Python",
        title = "Python Object Oriented Programming 101 with worked examples",
        date = date.today(),
        description = "I felt myself struggling with getting my head around OOP during class but the examples in this walkthrough were good! Hope this can help someone else too!",
        link = "https://realpython.com/python3-object-oriented-programming/"
    )
    db.session.add(thread3)
    # commit the changes
    db.session.commit()
    print("Table seeded") 

@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")