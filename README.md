# T2A2 - API Web Server Project - CramHub
Hello! Thanks for visiting the CramHub repository!

CramHub is a web server and API project that allows anyone studying coding concepts to submit any content they've found online and letting other students add a rating and review with the aim that meaningful and helpful content that is highly rated by peers can be easily found.

---
## Directory
R0 - [Install guide (WSL)](#r0---install-guide-wsl)

R1 - [Problem I'm trying to solve](#r1---problem-im-trying-to-solve)

R2 - [Why does it need solving?](#r2---why-does-it-need-solving)

R3 - [Why did I choose this database system (and comparison to others)?](#r3---why-did-i-choose-this-database-system-and-comparison-to-others)

R4 - [Key functionalities and benefits of an ORM](#r4---key-functionalities-and-benefits-of-an-orm)

R5 - [API Endpoints](#r5---api-endpoints)

R6 - [ERD](#r6---erd)

R7 - [Third party services](#r7---third-party-services)

R8 - [Project models relationships](#r8---project-models-relationships)

R9 - [Database relations](#r9---database-relations)

R10 - [Project Management](#r10---project-management)

## R0 - Install guide (WSL)
#### Create Virtual Environment
- Open a WSL terminal and create a virtual environment
- `python3 -m venv .venv`
- Activate the virtual environment
- `source .venv/bin/activate`
- Open your IDE
- `code .`
- Install the dependencies
- `pip install -r requirements.txt`

#### Create a PostgreSQL database and admin user
- Open a WSL terminal and open PostgreSQL 
- `sudo -u postgres psql`
- Create a database
- `create database cramhub_db;`
- Create a database admin user with password (example credentials below)
- `create user cramhub_dev with password 'cramhub';`
- Grant all privileges to admin user
- `grant all privileges on database cramhub_db to cramhub_dev;`
- Grant all permissions on database schemas to admin user
- `grant all on schema public to cramhub_dev;`

#### Create tables, seed database and run Flask application
- Open a WSL terminal (exit out of PostgreSQL if still open)
- Create the tables
- `flask db create`
- Seed the tables with data
- `flask db seed`
- Run the Flask app
- `flask run`

#### Application Environment files
- Create a new `.flaskenv` file and change the included code in the `.flaskenv_sample` file to suit your needs
- Create a new `.env` file and change the included code in the `.env_sample` file to suit your needs
---

## R1 - Problem I'm trying to solve
Have you ever experienced the building internal dread of sitting in class thinking *'Gadzooks! I don't understand a thing about this topic'*? Yep, I've been there, **we've** been there.

After taking a few moments to pull yourself together while trying to hide your tears did you ever stare blankly out the classroom window (or at the Windows XP flowing meadows wallpaper) and think *'You know what would be awesome? If I could crowdsource my studies so I'm not wasting precious **Risk of Rain 2** time by trying to find something good to study!'*?

The CramHub project aims to crowdsource learning materials from students alike that were particularly helpful in helping them understand a particular concept. There is a peer-review angle that allows other students to give the material a go and give a rating and review with the aim that high quality content will be higher ranked allowing other students to quickly view the ratings and save time when trying to pick something to study.

For this particular application, my usecase has been for the CoderAcademy course syllabus thus far (and the allowable categories can be extended quite easily) for the benefit of the students undertaking this course. 

## R2 - Why does it need solving?
With the advent of the internet it's very easy to find information or materials with a few keystrokes and a mouse click allowing anyone to upskill if they put the time in; but alas, this is a double-edged sword. With heaping mounds of information comes a huge time investment trying to find material that fits the bill and not a word dump copied from StackOverflow for SEO optimisation. 

It's extremely time consuming to trawl through the huge mountain of guides, walkthroughs and YouTube videos to find something that is easily understandable with a clear and concise step-by-step approach.

The CramHub project aims to reduce this time investment that is required before any substantial learning can even begin.

## R3 - Why did I choose this database system (and comparison to others)? 

## R4 - Key functionalities and benefits of an ORM

## R5 - API Endpoints
- Users endpoints
    - [Register new user](#1-register-new-user)
    - [Login as existing user](#2-login-as-existing-user)
    - [Get all users](#3-get-all-users)
    - [Get all threads by all users](#4-get-all-threads-by-all-users)
    - [Get all threads by a single user (by user_id)](#5-get-all-threads-by-single-user-by-user_id)
    - [Get all comments by all users](#6-get-all-comments-by-all-users)

- Threads endpoints
    - [Get all threads](#7-get-all-comments-by-all-users)
    - [Get a single thread (by thread_id)](#8-get-a-single-thread-by-thread_id)
    - [Get all threads (by category)](#9-get-all-threads-by-category)
    - [Create new thread](#10-create-new-thread)
    - [Update existing thread (by thread_id)](#11-updating-existing-thread-by-thread_id)
    - [Delete existing thread (by thread_id)](#12-delete-existing-thread-by-thread_id)

- Comments endpoints 
    - [Get all comments](#13-get-all-comments)
    - [Create new comment on thread (by thread_id)](#14-create-new-comment-on-thread-by-thread_id)
    - [Update existing comment (by comment_id)](#15-update-existing-comment-by-comment_id)
    - [Delete existing comment (by comment_id)](#16-delete-existing-comment-by-comment_id)

### Users endpoints
#### 1. Register new user
- Endpoint: `/users/register`
- HTTP verb: `POST`
- Required data:
  - `name`
  - `password`
  - `email`
  - `cohort`
- Expected response:
  - `201 CREATED`
  - Return all data excluding: `password`, `admin`
  - Message: `User {name} has been registered! 🙂`
  - `Access token` (with 6 hour expiry)
- Authentication method: None
![Register new user](./docs/endpoint%20examples/register_new_user.png)
---

#### 2. Login as existing user
- Endpoint: `/users/login`
- HTTP verb: `POST`
- Required data:
  - `email`
  - `password`
- Expected response:
  - `200 OK`
  - Return `user` and `token`
  - Message: `Successfully logged in! 🙂`
- Authentication method: If the user exists, the submitted password will be hashed (via Bcrypt) and compared to the hashed password in the database
![Login as existing user](./docs/endpoint%20examples/login_as_existing_user.png)
---

#### 3. Get all users
- Endpoint: `/users`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return list of users excluding: `password`, `admin`, `threads`, `comments`
- Authentication method: `None`
![Get all user](./docs/endpoint%20examples/get_all_users.png)
---

#### 4. Get all threads by all users
- Endpoint: `/users/threads`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return list of users excluding: `id`, `password`, `admin`, `comments`
- Authentication method: `None`
![Get all threads by all users](./docs/endpoint%20examples/get_all_threads_by_all_users.png)
---

#### 5. Get all threads by single user (by user_id)
- Endpoint: `/users/<int:user_id>/threads`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return list of threads that belong to a single user excluding: `comments`
- Authentication method: `None`
![Get all threads by single user](./docs/endpoint%20examples/get_all_threads_by_single_user.png)
---

#### 6. Get all comments by all users
- Endpoint: `/users/comments`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return list of comments by all users
- Authentication method: `None`
![Get all comments by all users](./docs/endpoint%20examples/get_all_comments_by_all_users.png)
---

### Threads endpoints
#### 7. Get all threads
- Endpoint: `/threads`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return list of threads excluding: `comments`
- Authentication method: `None`
![Get all threads](./docs/endpoint%20examples/get_all_threads.png)
---

#### 8. Get a single thread (by thread_id)
- Endpoint: `/threads/<int:thread_id>`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return single thread
- Authentication method: `None`
![Get a single thread](./docs/endpoint%20examples/get_single_thread.png)
---

#### 9. Get all threads (by category)
- Endpoint: `/threads/<str:category>`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return all threads that match the requested category
- Authentication method: `None`
![Get all threads by category](./docs/endpoint%20examples/get_all_threads_by_category.png)
---

#### 10. Create new thread
- Endpoint: `/threads`
- HTTP verb: `POST`
- Required data:
  - `category` - must be one of the following categories: HTML, CSS, Python, SQL, Flask
  - `title`
  - `description`
  - `link`
- Expected resonse:
  - `201 CREATED`
  - Return thread data excluding: `user`, `comments`
  - Message: `Thread submitted! 🙂`
- Authentication: Current JWT
![Create new thread](./docs/endpoint%20examples/create_new_thread.png)
---

#### 11. Updating existing thread (by thread_id)
- Endpoint: `/threads/<int:thread_id>`
- HTTP verb: `PUT`, `PATCH`
- Required data:
  - `category` - must be one of: HTML, CSS, Python, SQL, Flask
  - `title`
  - `description`
  - `link`
- Expected resonse:
  - `200 OK`
  - Return updated thread data excluding: `date`, `user`, `comments`
  - Message: `Thread {title} has been updated! 🙂`
- Authentication: Current JWT, JWT user id must match user id that created original thread
![Update existing thread](./docs/endpoint%20examples/update_existing_thread.png)
---

#### 12. Delete existing thread (by thread_id)
- Endpoint: `/threads/<int:thread_id>`
- HTTP verb: `DELETE`
- Required data:`None`
- Expected resonse:
  - `200 OK`
  - Message: `Thread {title} deleted! 🙂`
- Authentication: Current JWT, JWT user id must match user id that created original thread
![Delete existing thread](./docs/endpoint%20examples/delete_existing_thread.png)
---

### Comments endpoints

#### 13. Get all comments
- Endpoint: `/comments`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return list of comments 
- Authentication method: `None`
![Get all comments](./docs/endpoint%20examples/get_all_comments.png)
---

#### 14. Create new comment on thread (by thread_id)
- Endpoint: `/threads/<int:thread_id>/comments`
- HTTP verb: `POST`
- Required data:
  - `rating` - must be integer and one of: 1, 2, 3, 4 or 5
  - `review`
- Expected resonse:
  - `201 CREATED`
  - Return comment data
  - Message: `Comment submitted! 🙂`
- Authentication: Current JWT
![Create new comment on thread](./docs/endpoint%20examples/create_new_comment.png)
---

#### 15. Update existing comment (by comment_id)
- Endpoint: `/comments/<int:comment_id>`
- HTTP verb: `PUT`, `PATCH`
- Required data:
  - `rating`
  - `review`
- Expected resonse:
  - `200 OK`
  - Return updated thread data excluding: `user`
  - Message: `Comment with ID: '{comment_id}' has been updated! 🙂`
- Authentication: Current JWT, JWT user id must match user id that created original comment
![Update existing comment](./docs/endpoint%20examples/update_existing_comment.png)
---

#### 16. Delete existing comment (by comment_id)
- Endpoint: `/comments/<int:comment_id>`
- HTTP verb: `DELETE`
- Required data:`None`
- Expected resonse:
  - `200 OK`
  - Message: `Comment with ID: '{comment_id}' deleted! 🙂`
- Authentication: Current JWT, JWT user id must match user id that created original comment
![Delete existing comment](./docs/endpoint%20examples/delete_existing_comment.png)
---

## R6 - ERD

![Cramhub ERD](./docs/cramhubERD.png)

## R7 - Third party services

## R8 - Project models relationships

## R9 - Database relations

## R10 - Project Management