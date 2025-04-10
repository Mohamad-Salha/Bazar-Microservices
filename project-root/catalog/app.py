from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

# Define the path to the CSV file
CATALOG_FILE = 'catalog.txt'


def read_catalog():
    """Reads the catalog from the text file and returns it as a list of dictionaries."""
    books = []
    with open(CATALOG_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            books.append({
                'id': int(row[0]),
                'title': row[1],
                'cost': float(row[2]),
                'stock': int(row[3]),
                'topic': row[4]
            })
    return books


def write_catalog(books):
    """Writes the list of books back to the text file."""
    with open(CATALOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        for book in books:
            writer.writerow([book['id'], book['title'], book['cost'], book['stock'], book['topic']])


@app.route('/search', methods=['GET'])
def search_by_topic():
    topic = request.args.get('topic')
    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    books = read_catalog()
    filtered_books = {book['title']: book['id'] for book in books if book['topic'] == topic}

    return jsonify({"items": filtered_books})


@app.route('/info/<item_number>', methods=['GET'])
def info(item_number):
    books = read_catalog()
    book = next((book for book in books if book['id'] == int(item_number)), None)

    if book:
        return jsonify(book)
    return jsonify({"error": "Item not found"}), 404


@app.route('/update/<item_number>', methods=['POST'])
def update_stock(item_number):
    data = request.get_json()
    new_stock = data.get('stock')
    if new_stock is None:
        return jsonify({"error": "Stock value is required"}), 400

    books = read_catalog()
    book = next((book for book in books if book['id'] == int(item_number)), None)

    if book:
        book['stock'] = new_stock
        write_catalog(books)
        return jsonify({"message": "Stock updated successfully"}), 200

    return jsonify({"error": "Item not found"}), 404


if __name__ == '__main__':
    app.run(host='localhost', port=5001)
