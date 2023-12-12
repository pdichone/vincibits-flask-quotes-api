from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample Data
quotes = [
    {
        "id": 1,
        "author": "Albert Einstein",
        "quote": "Life is like riding a bicycle. To keep your balance, you must keep moving.",
    },
    {
        "id": 2,
        "author": "Mark Twain",
        "quote": "The secret of getting ahead is getting started.",
    },
]


# Route to get all quotes
@app.route("/quotes", methods=["GET"])
def get_quotes():
    return jsonify(quotes)


# Route to get a specific quote
@app.route("/quotes/<int:id>", methods=["GET"])
def get_quote(id):
    quote = next((q for q in quotes if q["id"] == id), None)
    return jsonify(quote) if quote else ("", 404)


# Route to add a new quote
@app.route("/quotes", methods=["POST"])
def add_quote():
    new_quote = request.json
    quotes.append(new_quote)
    return jsonify(new_quote), 201


# Route to delete a quote
@app.route("/quotes/<int:id>", methods=["DELETE"])
def delete_quote(id):
    # list comprehension to remove an item fro the quotes list
    # creates a new list that includes every quote in
    # the original quotes list except for the quote whose 'id' matches
    # the specified id. This effectively "removes" the quote with the matching 'id' from
    # the quotes list.
    global quotes  # add this so we have access to the quotes list, for now!
    quotes = [q for q in quotes if q["id"] != id]
    return "", 204


# Route to update a quote
@app.route("/quotes/<int:id>", methods=["PUT"])
def update_quote(id):
    print(f"REQESTE== {request.json}")
    quote = next((q for q in quotes if q["id"] == id), None)
    if quote:
        quote.update(request.json)
        return jsonify(quote)
    return "", 404


# for reload use flask --debug run

if __name__ == "__main__":
    app.run(debug=True)
