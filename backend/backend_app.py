from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)

SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Masterblog API"
    }
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

POSTS = [
    {
        "id": 1,
        "title": "First post",
        "content": "This is the first post.",
        "author": "Merve",
        "date": "2026-03-19"
    },
    {
        "id": 2,
        "title": "Second post",
        "content": "This is the second post.",
        "author": "Baha",
        "date": "2026-03-20"
    }
]


def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False


@app.route("/api/posts", methods=["GET"])
def get_posts():
    sort_field = request.args.get("sort")
    direction = request.args.get("direction")

    if sort_field is None and direction is None:
        return jsonify(POSTS), 200

    if sort_field is None:
        return jsonify({
            "message": "Invalid sort field. Allowed values are 'title', 'content', 'author' or 'date'."
        }), 400

    valid_sort_fields = ["title", "content", "author", "date"]

    if sort_field not in valid_sort_fields:
        return jsonify({
            "message": "Invalid sort field. Allowed values are 'title', 'content', 'author' or 'date'."
        }), 400

    if direction is None:
        direction = "asc"

    if direction not in ["asc", "desc"]:
        return jsonify({
            "message": "Invalid direction. Allowed values are 'asc' or 'desc'."
        }), 400

    reverse_sort = direction == "desc"

    if sort_field == "date":
        sorted_posts = sorted(
            POSTS,
            key=lambda post: datetime.strptime(post["date"], "%Y-%m-%d"),
            reverse=reverse_sort
        )
    else:
        sorted_posts = sorted(
            POSTS,
            key=lambda post: str(post[sort_field]).lower(),
            reverse=reverse_sort
        )

    return jsonify(sorted_posts), 200


@app.route("/api/posts", methods=["POST"])
def add_post():
    daten = request.get_json(silent=True)

    if daten is None:
        return jsonify({
            "fehler": "Keine gültigen JSON-Daten erhalten.",
            "fehlende_felder": ["title", "content", "author", "date"]
        }), 400

    fehlende_felder = []

    required_fields = ["title", "content", "author", "date"]

    for feld in required_fields:
        if feld not in daten or not str(daten[feld]).strip():
            fehlende_felder.append(feld)

    if fehlende_felder:
        return jsonify({
            "fehler": "Erforderliche Felder fehlen.",
            "fehlende_felder": fehlende_felder
        }), 400

    if not is_valid_date(daten["date"]):
        return jsonify({
            "fehler": "Invalid date format. Use YYYY-MM-DD."
        }), 400

    neue_id = max(post["id"] for post in POSTS) + 1 if POSTS else 1

    neuer_post = {
        "id": neue_id,
        "title": daten["title"],
        "content": daten["content"],
        "author": daten["author"],
        "date": daten["date"]
    }

    POSTS.append(neuer_post)

    return jsonify(neuer_post), 201


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    for post in POSTS:
        if post["id"] == post_id:
            POSTS.remove(post)
            return jsonify({
                "message": f"Post with id {post_id} has been deleted successfully."
            }), 200

    return jsonify({
        "message": f"Post with id {post_id} was not found."
    }), 404


@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    daten = request.get_json(silent=True)

    for post in POSTS:
        if post["id"] == post_id:
            if daten is not None:
                if "title" in daten:
                    post["title"] = daten["title"]
                if "content" in daten:
                    post["content"] = daten["content"]
                if "author" in daten:
                    post["author"] = daten["author"]
                if "date" in daten:
                    if not is_valid_date(daten["date"]):
                        return jsonify({
                            "fehler": "Invalid date format. Use YYYY-MM-DD."
                        }), 400
                    post["date"] = daten["date"]

            return jsonify(post), 200

    return jsonify({
        "message": f"Post with id {post_id} was not found."
    }), 404


@app.route("/api/posts/search", methods=["GET"])
def search_posts():
    search_query = request.args.get("search", "").strip().lower()

    title_query = request.args.get("title", "").strip().lower()
    content_query = request.args.get("content", "").strip().lower()
    author_query = request.args.get("author", "").strip().lower()
    date_query = request.args.get("date", "").strip().lower()

    ergebnisse = []

    for post in POSTS:
        general_match = True
        if search_query:
            general_match = (
                search_query in post["title"].lower()
                or search_query in post["content"].lower()
                or search_query in post["author"].lower()
                or search_query in post["date"].lower()
            )

        title_match = title_query in post["title"].lower() if title_query else True
        content_match = content_query in post["content"].lower() if content_query else True
        author_match = author_query in post["author"].lower() if author_query else True
        date_match = date_query in post["date"].lower() if date_query else True

        if general_match and title_match and content_match and author_match and date_match:
            ergebnisse.append(post)

    return jsonify(ergebnisse), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)