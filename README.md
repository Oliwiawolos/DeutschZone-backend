# DeutschZone Backend
- [General Info](#general-info)
- [Technologies Used](#technologies-used)
- [Installation and Setup](#installation-and-setup)
- [API Endpoints](#API-endpoints)

## General Info
This is the backend for the DeutschZone web app. It is built with Flask and connects to a PostgreSQL database. It provides RESTful APIs for managing users, folders, and flashcards.

## Technologies Used
* Python (Flask)
* PostgreSQL
* SQLAlchemy
* Docker
* psycopg2
* CORS

## Installation and Setup
1. Clone the repository: `git clone https://github.com/Oliwiawolos/DeutschZone-backend.git`
2. Navigate to the project’s root directory
3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file in the project root based on the following example: `SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost:5432/flashcards`
5. Run the backend: `python app.py`
6. The server will be running at: `http://localhost:5000`

### If you prefer Docker-based development: 
1. Make sure you have a Dockerfile in the project root.
2. Create a `.env` file in the project root with the following content: `SQLALCHEMY_DATABASE_URI=postgresql://user:password@db:5432/flashcards`
> **Note:** `db` should match the hostname of your PostgreSQL service in `docker-compose.yml`.
3. Build the Docker image: `docker build -t projektowanie-backend .` 
4. Run the container: `docker run --env-file .env -p 5000:5000 projektowanie-backend` 
5. Navigate to: `http://localhost:5000`.

### API Endpoints
* /register: Register a new user.
* /login: Log in a user and return authentication tokens.
* /flashcards: API for adding, retrieving, updating, and deleting flashcards.
* /folders: API for managing flashcard folders.
* /sync-user: Sync user data with the frontend.
