from main import db
from flask import Blueprint
from models.users import User
from models.threads import Thread
from models.comments import Comment
from datetime import date
from main import bcrypt


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
        password = bcrypt.generate_password_hash("password").decode("utf-8"),
        email = "admin@cramhub.com",
        cohort = "Admin Team",
        admin = True
    )
    db.session.add(admin_user)

    # User 1
    user1 = User(
        name = "Ayrton Senna",
        password = bcrypt.generate_password_hash("honda4eva").decode("utf-8"),
        email = "senna@gmail.com",
        cohort = "2023 September Accelerated",
    )
    db.session.add(user1)
    
    # User 2
    user2 = User(
        name = "Harry Potter",
        password = bcrypt.generate_password_hash("hunter2").decode("utf-8"),
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

    # Comment 1
    comment1 = Comment(
        date = date.today(),
        rating = 5,
        review = "I really found this one helpful, thanks!"
    )
    db.session.add(comment1)

    # Comment 2
    comment2 = Comment(
        date = date.today(),
        rating = 2,
        review = "This one didn't really do it for me"
    )
    db.session.add(comment2)

    # Comment 3
    comment3 = Comment(
        date = date.today(),
        rating = 4,
        review = "Good resource. Had to do extra research on this but overall quite a good guide!"
    )
    db.session.add(comment3)
    
    # Commit the added entries
    db.session.commit()
    print("Table seeded") 

@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")