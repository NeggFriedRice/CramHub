from flask import Blueprint
from datetime import date
from init import bcrypt, db
from models.comments import Comment
from models.users import User
from models.threads import Thread

# DB commands blueprint registered in main
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
        name = "User 1",
        password = bcrypt.generate_password_hash("honda4eva").decode("utf-8"),
        email = "user1@email.com",
        cohort = "2023 September Accelerated",
    )
    db.session.add(user1)
    
    # User 2
    user2 = User(
        name = "User 2",
        password = bcrypt.generate_password_hash("hunter2").decode("utf-8"),
        email = "user2@email.com",
        cohort = "2023 May Standard",
    )
    db.session.add(user2)
    db.session.commit()

    # User 3
    user3 = User(
        name = "Commenter 1",
        password = bcrypt.generate_password_hash("pizzaislife").decode("utf-8"),
        email = "commenter1@email.com",
        cohort = "2023 October Standard",
    )
    db.session.add(user3)
    db.session.commit()

    # User 4
    user4 = User(
        name = "Commenter 2",
        password = bcrypt.generate_password_hash("pastaislife").decode("utf-8"),
        email = "commenter2@email.com",
        cohort = "2023 September Accelerated",
    )
    db.session.add(user4)
    db.session.commit()

    # Thread 1
    thread1 = Thread(
        category = "HTML",
        title = "HTML Basics",
        date = date.today(),
        description = "Good introduction to HTML5 that really helped me understand the basics of what HTML is and what we can do with it",
        link = "https://www.youtube.com/watch?v=8_YadxRXGaA",
        user_id = user1.id
    )
    db.session.add(thread1)

    # Thread 2
    thread2 = Thread(
        category = "CSS",
        title = "Cool animations with CSS",
        date = date.today(),
        description = "Found this website that has a list of cool animations you can do with CSS. Will be adding some of these to my portfolio",
        link = "https://www.w3schools.com/css/css3_animations.asp",
        user_id = user1.id
    )
    db.session.add(thread2)

    # Thread 3
    thread3 = Thread(
        category = "Python",
        title = "Python Object Oriented Programming 101 with worked examples",
        date = date.today(),
        description = "I felt myself struggling with getting my head around OOP during class but the examples in this walkthrough were good! Hope this can help someone else too!",
        link = "https://realpython.com/python3-object-oriented-programming/",
        user_id = user2.id
    )
    db.session.add(thread3)
    db.session.commit()

    # Comment 1
    comment1 = Comment(
        date = date.today(),
        rating = 5,
        review = "I really found this one helpful, thanks!",
        user_id = user3.id,
        thread_id = thread1.id
    )
    db.session.add(comment1)

    # Comment 2
    comment2 = Comment(
        date = date.today(),
        rating = 2,
        review = "This one didn't really do it for me",
        user_id = user4.id,
        thread_id = thread1.id
    )
    db.session.add(comment2)

    # Comment 3
    comment3 = Comment(
        date = date.today(),
        rating = 4,
        review = "Good resource. Had to do extra research on this but overall quite a good guide!",
        user_id = user3.id,
        thread_id = thread2.id
    )
    db.session.add(comment3)
    
    # Commit the added entries
    db.session.commit()
    print("Table seeded") 

@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")