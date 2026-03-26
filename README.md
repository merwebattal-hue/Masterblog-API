# Masterblog API

A Flask-based RESTful blog API built as part of a backend development exercise.

## Features

- List blog posts
- Add new posts
- Update existing posts
- Delete posts
- Search posts
- Sort posts
- Swagger API documentation
- JSON file persistence
- Extended post model with:
  - title
  - content
  - author
  - date

## Tech Stack

- Python
- Flask
- Flask-CORS
- Flask-Swagger-UI
- JSON file storage

## API Endpoints

- `GET /api/posts`
- `POST /api/posts`
- `PUT /api/posts/<post_id>`
- `DELETE /api/posts/<post_id>`
- `GET /api/posts/search`
- `GET /api/docs`

## Run the Project

Install dependencies:

```bash
pip3 install -r requirements.txt
