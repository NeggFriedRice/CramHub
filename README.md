# T2A2 - API Web Server Project - CramHub

R1 - Identification of problem
R2 - Why is it a problem that needs solving?
R3 - Why have you chosen this database system? What are the drawbacks compared to others?
R4 - Idetify and discuss the key functionalities and benefits of an ORM

# R5 - API Endpoints
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

#### 3. Get all users
- Endpoint: `/users`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return list of users excluding: `id`, `password`, `admin`, `threads`, `comments`
- Authentication method: `None`

#### 4. Get all threads by all users
- Endpoint: `/users/threads`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return list of users excluding: `id`, `password`, `admin`, `comments`
- Authentication method: `None`

#### 5. Get all threads by single user (by user_id)
- Endpoint: `/users/<int:user_id>/threads`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return list of threads that belong to a single user excluding: `comments`
- Authentication method: `None`

#### 6. Get all comments by all users
- Endpoint: `/users/comments`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return list of comments
- Authentication method: `None`

### Threads endpoints
#### 7. Get all threads
- Endpoint: `/threads`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return list of threads excluding: `comments`
- Authentication method: `None`

#### 8. Get a single thread (by thread_id)
- Endpoint: `/threads/<int:thread_id>`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return single thread
- Authentication method: `None`

#### 9. Get all threads (by category)
- Endpoint: `/threads/<str:category>`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return all threads that match the requested category
- Authentication method: `None`

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

#### 12. Delete existing thread (by thread_id)
- Endpoint: `/threads/<int:thread_id>`
- HTTP verb: `DELETE`
- Required data:`None`
- Expected resonse:
  - `200 OK`
  - Message: `Thread {title} deleted! 🙂`
- Authentication: Current JWT, JWT user id must match user id that created original thread

### Comments endpoints

#### 13. Get all comments
- Endpoint: `/comments`
- HTTP verb: `GET`
- Required data: `None`
- Expected response:
  - `200 OK`
  - Return list of comments 
- Authentication method: `None`

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
- Authentication: Current JWT, JWT user id must match user id that created original thread

#### 16. Delete existing comment (by comment_id)
- Endpoint: `/comments/<int:comment_id>`
- HTTP verb: `DELETE`
- Required data:`None`
- Expected resonse:
  - `200 OK`
  - Message: `Comment with ID: '{comment_id}' deleted! 🙂`
- Authentication: Current JWT, JWT user id must match user id that created original thread
R6 - ERD
R7 - Third party services
R8 - Describe project models in terms of relationships
R9 - Describe the database relations implemented in your application
R10 - Describe the way tasks are allocated and tracked