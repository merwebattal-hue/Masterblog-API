from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route("/api/posts", methods=["GET"])
def get_posts():
    return jsonify(POSTS), 200


@app.route("/api/posts", methods=["POST"])
def add_post():
    daten = request.get_json(silent=True)

    if daten is None:
        return jsonify({
            "fehler": "Keine gültigen JSON-Daten erhalten.",
            "fehlende_felder": ["title", "content"]
        }), 400

    fehlende_felder = []

    if "title" not in daten or not str(daten["title"]).strip():
        fehlende_felder.append("title")

    if "content" not in daten or not str(daten["content"]).strip():
        fehlende_felder.append("content")

    if fehlende_felder:
        return jsonify({
            "fehler": "Erforderliche Felder fehlen.",
            "fehlende_felder": fehlende_felder
        }), 400

    neue_id = max(post["id"] for post in POSTS) + 1 if POSTS else 1

    neuer_post = {
        "id": neue_id,
        "title": daten["title"],
        "content": daten["content"]
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

            return jsonify(post), 200

    return jsonify({
        "message": f"Post with id {post_id} was not found."
    }), 404


@app.route("/api/posts/search", methods=["GET"])
def search_posts():
    title_query = request.args.get("title", "").strip().lower()
    content_query = request.args.get("content", "").strip().lower()

    ergebnisse = []

    for post in POSTS:
        title_match = title_query in post["title"].lower() if title_query else True
        content_match = content_query in post["content"].lower() if content_query else True

        if title_match and content_match:
            ergebnisse.append(post)

    return jsonify(ergebnisse), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)