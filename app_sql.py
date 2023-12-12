from flask import Flask, jsonify, request, g
import sqlite3

app_sql = Flask(__name__)
DATABASE = "quotes.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = (
        sqlite3.Row
    )  # This enables column access by name: row['column_name']
    return db


@app_sql.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    with app_sql.app_context():
        db = get_db()
        with app_sql.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


# Run this function to initialize the database
init_db()


# Routes
@app_sql.route("/quotes", methods=["GET"])
def get_quotes():
    db = get_db()
    quotes = db.execute("SELECT * FROM quotes").fetchall()
    return jsonify([dict(q) for q in quotes])


@app_sql.route("/quotes/<int:id>", methods=["GET"])
def get_quote(id):
    db = get_db()
    quote = db.execute("SELECT * FROM quotes WHERE id = ?", (id,)).fetchone()
    return jsonify(dict(quote)) if quote else ("", 404)


@app_sql.route("/quotes", methods=["POST"])
def add_quote():
    db = get_db()
    new_quote = request.json
    db.execute(
        "INSERT INTO quotes (author, quote) VALUES (?, ?)",
        (new_quote["author"], new_quote["quote"]),
    )
    db.commit()
    return jsonify(new_quote), 201


@app_sql.route("/quotes/<int:id>", methods=["PUT"])
def update_quote(id):
    db = get_db()
    updated_quote = request.json
    db.execute(
        "UPDATE quotes SET author = ?, quote = ? WHERE id = ?",
        (updated_quote["author"], updated_quote["quote"], id),
    )
    db.commit()
    return jsonify(updated_quote)


@app_sql.route("/quotes/<int:id>", methods=["DELETE"])
def delete_quote(id):
    db = get_db()
    db.execute("DELETE FROM quotes WHERE id = ?", (id,))
    db.commit()
    return ("", 204)


if __name__ == "__main__":
    app_sql.run(debug=True)
