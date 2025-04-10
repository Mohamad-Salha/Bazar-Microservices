import csv
import json
import os
from flask import Flask, jsonify, request
from database import Book, get_db_engine, get_db_session, init_db, import_books_from_csv

app = Flask(__name__)

# Path to the CSV file storing book data (for initial import)
BOOKS_FILE = 'books.csv'


# Initialize database
engine = get_db_engine('catalog')
init_db(engine)

# Import books from CSV if database is empty
def initialize_db():
    session = get_db_session(engine)
    book_count = session.query(Book).count()
    if book_count == 0 and os.path.exists(BOOKS_FILE):
        import_books_from_csv(session, BOOKS_FILE)
    session.close()

# Initialize database on startup
initialize_db()

def read_books():
    """Read books data from database"""
    session = get_db_session(engine)
    books = [book.to_dict() for book in session.query(Book).all()]
    session.close()
    return books


def get_book_by_id(item_number):
    """Get a book by its item number"""
    session = get_db_session(engine)
    book = session.query(Book).filter(Book.item_number == item_number).first()
    result = book.to_dict() if book else None
    session.close()
    return result

def update_book(item_number, data):
    """Update a book in the database"""
    session = get_db_session(engine)
    book = session.query(Book).filter(Book.item_number == item_number).first()
    if not book:
        session.close()
        return False
    
    if 'stock' in data:
        book.stock = int(data['stock'])
    if 'cost' in data:
        book.cost = int(data['cost'])
    
    session.commit()
    session.close()
    return True


@app.route('/query/subject/<topic>', methods=['GET'])
def query_by_subject(topic):
    """Query books by subject/topic"""
    books = read_books()
    matching_books = [book for book in books if book['topic'].lower() == topic.lower()]
    
    # Format response as per the requirements
    result = {"items": {}}
    for book in matching_books:
        result["items"][book['title']] = book['item_number']
    
    return jsonify(result)


@app.route('/query/keyword/<keyword>', methods=['GET'])
def query_by_keyword(keyword):
    """Query books by any keyword in title or topic"""
    books = read_books()
    keyword = keyword.lower()
    matching_books = [book for book in books if 
                     keyword in book['title'].lower() or 
                     keyword in book['topic'].lower()]
    
    # Format response as per the requirements
    result = {"items": {}}
    for book in matching_books:
        result["items"][book['title']] = book['item_number']
    
    return jsonify(result)


@app.route('/query/item/<int:item_number>', methods=['GET'])
def query_by_item(item_number):
    """Query book details by item number"""
    book = get_book_by_id(item_number)
    if book:
        return jsonify(book)
    
    return jsonify({"error": "Book not found"}), 404


@app.route('/update/<int:item_number>', methods=['PUT'])
def update_item(item_number):
    """Update book details (stock or cost)"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    success = update_book(item_number, data)
    
    if not success:
        return jsonify({"error": "Book not found"}), 404
    
    return jsonify({"success": True, "message": "Book updated successfully"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)