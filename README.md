Here is a concise and well-structured `README.md` for your project:

```markdown
# BookBear

BookBear is a Django-based API for managing books, authors, publishers, genres, and user interactions. It provides features for user authentication, book reviews, and managing relationships between users and entities like authors, publishers, and genres.

## Features

- **User Management**: Registration, login, profile updates, and avatar management.
- **Book Management**: CRUD operations for books, including uploading and deleting book covers.
- **Author Management**: CRUD operations for authors, including uploading and deleting author avatars.
- **Publisher Management**: CRUD operations for publishers.
- **Genre Management**: CRUD operations for genres.
- **User Interactions**: Follow authors, publishers, favorite genres, and manage user-book relationships (e.g., reviews, ratings).
- **Authentication**: JWT-based authentication with token refresh and password reset functionality.

## Tech Stack

- **Backend**: Django 5.2, Ninja-Extra
- **Database**: SQLite (default, can be replaced with other databases)
- **Authentication**: JWT (via `dj_ninja_auth`)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd BookBear
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- **POST** `/auth/register`: Register a new user.
- **POST** `/auth/login`: Login and obtain JWT tokens.
- **POST** `/auth/logout`: Logout the current user.
- **GET** `/auth/me`: Get the current user's details.

### Books
- **GET** `/book/`: List all books.
- **GET** `/book/{book_id}`: Get details of a specific book.
- **POST** `/admin/book`: Create a new book (Admin only).
- **PATCH** `/admin/book/{book_id}`: Update a book (Admin only).
- **DELETE** `/admin/book/{book_id}`: Delete a book (Admin only).

### Authors
- **POST** `/admin/author`: Create a new author (Admin only).
- **PATCH** `/admin/author/{author_id}`: Update an author (Admin only).
- **DELETE** `/admin/author/{author_id}`: Delete an author (Admin only).

### Publishers & Genres
- Similar CRUD endpoints for publishers and genres.

## Environment Variables

Create a `.env` file in the root directory and configure the following variables:

```env
SECRET_KEY=<your-secret-key>
AUTH_JWT_ACCESS_TOKEN_LIFETIME=5
AUTH_JWT_REFRESH_TOKEN_LIFETIME=1
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## Running Tests

Run the test suite using:
```bash
python manage.py test
```

## License

This project is licensed under the MIT License.
```

This `README.md` provides a quick overview of the project, its features, and setup instructions.