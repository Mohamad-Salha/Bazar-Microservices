import json
import time
import uuid
import requests
import os
from flask import Flask, jsonify, request
from database import Order, get_db_engine, get_db_session, init_db, import_orders_from_csv

app = Flask(__name__)

# Path to the CSV file storing order data (for initial import)
ORDERS_FILE = 'orders.csv'

# Catalog service URL
CATALOG_SERVICE_URL = os.environ.get('CATALOG_SERVICE_URL', 'http://localhost:5001')


# Initialize database
engine = get_db_engine('order')
init_db(engine)

# Import orders from CSV if database is empty
def initialize_db():
    session = get_db_session(engine)
    order_count = session.query(Order).count()
    if order_count == 0 and os.path.exists(ORDERS_FILE):
        import_orders_from_csv(session, ORDERS_FILE)
    session.close()

# Initialize database on startup
initialize_db()

def read_orders():
    """Read orders data from database"""
    session = get_db_session(engine)
    orders = [order.to_dict() for order in session.query(Order).all()]
    session.close()
    return orders


def write_order(order):
    """Add a new order to the database"""
    session = get_db_session(engine)
    new_order = Order(
        order_id=order['order_id'],
        item_number=int(order['item_number']),
        timestamp=order['timestamp']
    )
    session.add(new_order)
    session.commit()
    session.close()


@app.route('/purchase/<int:item_number>', methods=['POST'])
def purchase(item_number):
    """Process a purchase order"""
    # Check if the item is in stock by querying the catalog service
    catalog_response = requests.get(f'{CATALOG_SERVICE_URL}/query/item/{item_number}')
    
    if catalog_response.status_code != 200:
        return jsonify({"error": "Failed to retrieve book information"}), 500
    
    book = catalog_response.json()
    
    # Check if the book is in stock
    if book.get('stock', 0) <= 0:
        return jsonify({"error": "Book is out of stock"}), 400
    
    # Decrement the stock by 1
    update_data = {"stock": book['stock'] - 1}
    update_response = requests.put(
        f'{CATALOG_SERVICE_URL}/update/{item_number}',
        json=update_data,
        headers={"Content-Type": "application/json"}
    )
    
    if update_response.status_code != 200:
        return jsonify({"error": "Failed to update book stock"}), 500
    
    # Create a new order
    order = {
        "order_id": str(uuid.uuid4()),
        "item_number": str(item_number),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save the order
    write_order(order)
    
    return jsonify({
        "success": True,
        "message": "Purchase successful",
        "order": order
    })


if __name__ == '__main__':
    # Ensure orders file exists
    read_orders()
    app.run(host='0.0.0.0', port=5002, debug=True)