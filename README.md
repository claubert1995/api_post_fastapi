FastAPI Blog Application
This is a personal project designed to learn FastAPI. It is a blog application that allows users to write and publish blog posts. Multiple users can sign up and post their own articles.

Features

User registration and login
Create, read, and manage blog posts
JWT authentication for secure access to protected routes
Simple and easy-to-use REST API built with FastAPI

Requirements
Python 3.8+
FastAPI
Uvicorn (for running the app)
SQLAlchemy (for database interaction)
JWT for authentication
Installation Clone the repository:  git clone https://github.com/your-username/fastapi-blog.git
Install dependencies: pip install -r requirements.txt

Running the Application
To run the application locally, use Uvicorn:

uvicorn main:app --reload
The application will be accessible at http://127.0.0.1:8000.

API Endpoints
POST /register: Register a new user
POST /login: Login and obtain a JWT token
GET /posts: Get all blog posts
POST /posts: Create a new blog post (requires authentication)
GET /posts/{post_id}: Get a specific blog post by ID
PUT /posts/{post_id}: Update a blog post (requires authentication)
DELETE /posts/{post_id}: Delete a blog post (requires authentication)
Learning Objectives
Understanding FastAPI and its features
Implementing authentication with JWT tokens
Using SQLAlchemy for database management
Building a simple but functional REST API
License
This project is open-source and available under the MIT License.

