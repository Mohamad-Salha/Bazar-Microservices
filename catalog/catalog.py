from flask import Flask, jsonify, request
import os

app = Flask(__name__)
BOOKS_FILE = "catalog.txt"
books = {}


def load_books():
    global books
    books.clear()
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 5:
                    item_number = int(parts[0])
                    books[item_number] = {
                        "title": parts[1],
                        "topic": parts[2],
                        "stock": int(parts[3]),
                        "cost": int(parts[4]),
                    }


def save_books(books):
    with open(BOOKS_FILE, "w") as f:
        for item_number, info in books.items():
            f.write(
                f"{item_number},{info['title']},{info['topic']},{info['stock']},{info['cost']}\n"
            )


@app.route("/search/<topic>", methods=["GET"])
def search(topic):
    load_books()
    print(f"[CATALOG] Received request: /search/{topic}")
    result = [
        {"item_number": num, "title": info["title"]}
        for num, info in books.items()
        if info["topic"].lower().strip() == topic.lower().strip()
    ]
    return jsonify(result), 200


@app.route("/info/<int:item_number>", methods=["GET"])
def info(item_number):
    load_books()
    print(f"[CATALOG] Received request: /info/{item_number}")
    book = books.get(item_number)
    if not book:
        return jsonify({"error": "Item not found"}), 404
    return (
        jsonify(
            {
                "item_number": item_number,
                "title": book["title"],
                "stock": book["stock"],
                "cost": book["cost"],
            }
        ),
        200,
    )


@app.route("/decrease_stock/<int:item_number>", methods=["POST"])
def decrease_stock(item_number):
    load_books()  # Don't assign!
    if item_number in books:
        if books[item_number]["stock"] > 0:
            books[item_number]["stock"] -= 1
            print(f"[CATALOG] Decreased stock for item {item_number}")
            save_books(books)
            return (
                jsonify({"status": "success", "stock": books[item_number]["stock"]}),
                200,
            )
        else:
            return jsonify({"status": "fail", "message": "Out of stock"}), 400
    return jsonify({"status": "fail", "message": "Item not found"}), 404


@app.route("/update/<int:item_number>", methods=["POST"])
def update_book(item_number):
    load_books()
    data = request.get_json()

    if item_number not in books:
        return jsonify({"status": "fail", "message": "Item not found"}), 404

    updated = False
    if "stock" in data:
        books[item_number]["stock"] = int(data["stock"])
        updated = True
    if "cost" in data:
        books[item_number]["cost"] = int(data["cost"])
        updated = True

    if updated:
        save_books(books)
        print(f"[CATALOG] Updated book {item_number}: {data}")
        return jsonify({"status": "success", "message": "Book updated"}), 200
    else:
        return jsonify({"status": "fail", "message": "No valid fields to update"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
