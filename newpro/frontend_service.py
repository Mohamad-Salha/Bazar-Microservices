import requests
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Backend service URLs
import os
CATALOG_SERVICE_URL = os.environ.get('CATALOG_SERVICE_URL', 'http://localhost:5001')
ORDER_SERVICE_URL = os.environ.get('ORDER_SERVICE_URL', 'http://localhost:5002')


@app.route('/search/<topic>', methods=['GET'])
def search(topic):
    """Search books by topic"""
    # Forward the request to the catalog service
    response = requests.get(f'{CATALOG_SERVICE_URL}/query/subject/{topic}')
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to search books"}), 500
    
    return jsonify(response.json())


@app.route('/search_keyword/<keyword>', methods=['GET'])
def search_keyword(keyword):
    """Search books by any keyword in title or topic"""
    # Forward the request to the catalog service
    response = requests.get(f'{CATALOG_SERVICE_URL}/query/keyword/{keyword}')
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to search books"}), 500
    
    return jsonify(response.json())


@app.route('/info/<int:item_number>', methods=['GET'])
def info(item_number):
    """Get detailed information about a book"""
    # Forward the request to the catalog service
    response = requests.get(f'{CATALOG_SERVICE_URL}/query/item/{item_number}')
    
    if response.status_code != 200:
        return jsonify({"error": "Book not found"}), 404
    
    book_data = response.json()
    
    # Return HTML page with book details and purchase button
    return f"""
    <html>
        <head>
            <title>{book_data['title']} - Bazar.com</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }}
                h1, h2 {{ color: #333; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .book-details {{ background: #f9f9f9; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                .book-details p {{ margin: 10px 0; }}
                .purchase-btn {{ display: inline-block; padding: 10px 20px; background: #4CAF50; color: white; text-decoration: none; border-radius: 4px; font-weight: bold; cursor: pointer; border: none; }}
                .purchase-btn:hover {{ background: #45a049; }}
                .purchase-btn:disabled {{ background-color: #cccccc; cursor: not-allowed; }}
                .message {{ padding: 10px; border-radius: 4px; margin: 20px 0; }}
                .success {{ background-color: #dff0d8; color: #3c763d; }}
                .error {{ background-color: #f2dede; color: #a94442; }}
                .back-link {{ display: inline-block; margin-top: 20px; color: #666; text-decoration: none; }}
                .back-link:hover {{ color: #333; }}
            </style>
            <script>
                function purchaseBook(itemNumber) {{
                    fetch(`/purchase/${{itemNumber}}`, {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json'
                        }}
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        const messageDiv = document.getElementById('message');
                        messageDiv.style.display = 'block';
                        if (data.success) {{
                            messageDiv.className = 'message success';
                            messageDiv.textContent = 'Purchase successful! Your order has been placed.';
                            // Disable purchase button if stock is now 0
                            if (parseInt(document.getElementById('stock').textContent) <= 1) {{
                                document.getElementById('purchase-btn').disabled = true;
                                document.getElementById('purchase-btn').textContent = 'Out of Stock';
                                document.getElementById('stock').textContent = '0';
                            }} else {{
                                document.getElementById('stock').textContent = parseInt(document.getElementById('stock').textContent) - 1;
                            }}
                        }} else {{
                            messageDiv.className = 'message error';
                            messageDiv.textContent = data.error || 'Purchase failed. Please try again.';
                        }}
                    }})
                    .catch(error => {{
                        console.error('Error purchasing book:', error);
                        const messageDiv = document.getElementById('message');
                        messageDiv.style.display = 'block';
                        messageDiv.className = 'message error';
                        messageDiv.textContent = 'Error processing purchase. Please try again.';
                    }});
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <h1>Book Details</h1>
                
                <div class="book-details">
                    <h2>{book_data['title']}</h2>
                    <p><strong>Item Number:</strong> {book_data['item_number']}</p>
                    <p><strong>Topic:</strong> {book_data['topic']}</p>
                    <p><strong>Price:</strong> ${book_data['cost']}</p>
                    <p><strong>Stock:</strong> <span id="stock">{book_data['stock']}</span> available</p>
                    
                    <div id="message" class="message" style="display: none;"></div>
                    
                    <button 
                        id="purchase-btn" 
                        class="purchase-btn" 
                        onclick="purchaseBook({book_data['item_number']})" 
                        {{'disabled': 'true' if book_data['stock'] <= 0 else ''}}
                    >
                        {{'Out of Stock' if book_data['stock'] <= 0 else 'Purchase Now'}}
                    </button>
                </div>
                
                <a href="/" class="back-link">&larr; Back to Home</a>
            </div>
        </body>
    </html>
    """


@app.route('/purchase/<int:item_number>', methods=['POST'])
def purchase(item_number):
    """Purchase a book"""
    # Forward the request to the order service
    response = requests.post(f'{ORDER_SERVICE_URL}/purchase/{item_number}')
    
    if response.status_code != 200:
        return jsonify({"error": response.json().get("error", "Purchase failed")}), response.status_code
    
    return jsonify(response.json())


@app.route('/')
def index():
    """Simple home page with search form"""
    return """
    <html>
        <head>
            <title>Bazar.com - The World's Smallest Book Store</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }
                h1 { color: #333; }
                .container { max-width: 800px; margin: 0 auto; }
                .section { margin-bottom: 20px; }
                .api-endpoint { background: #f4f4f4; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
                .api-endpoint code { font-weight: bold; }
                .search-form { background: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                .search-form input[type="text"] { padding: 8px; width: 70%; border: 1px solid #ddd; border-radius: 4px; }
                .search-form button { padding: 8px 15px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; }
                .search-form button:hover { background: #45a049; }
                .search-results { margin-top: 20px; }
            </style>
            <script>
                function searchBooks() {
                    const topic = document.getElementById('search-topic').value.trim();
                    if (!topic) return;
                    
                    fetch(`/search/${topic}`)
                        .then(response => response.json())
                        .then(data => {
                            const resultsDiv = document.getElementById('search-results');
                            resultsDiv.innerHTML = '';
                            
                            if (data.items && Object.keys(data.items).length > 0) {
                                const resultsList = document.createElement('ul');
                                for (const [title, itemNumber] of Object.entries(data.items)) {
                                    const listItem = document.createElement('li');
                                    listItem.innerHTML = `<a href="/info/${itemNumber}">${title}</a> (Item #${itemNumber})`;
                                    resultsList.appendChild(listItem);
                                }
                                resultsDiv.appendChild(resultsList);
                            } else {
                                resultsDiv.innerHTML = '<p>No books found for this topic.</p>';
                            }
                        })
                        .catch(error => {
                            console.error('Error searching books:', error);
                            document.getElementById('search-results').innerHTML = '<p>Error searching books. Please try again.</p>';
                        });
                    
                    return false;
                }
            </script>
        </head>
        <body>
            <div class="container">
                <h1>Bazar.com - The World's Smallest Book Store</h1>
                
                <div class="section search-form">
                    <h2>Search Books by Topic</h2>
                    <form onsubmit="return searchBooks()">
                        <input type="text" id="search-topic" placeholder="Enter a topic (e.g. distributed systems)" required>
                        <button type="submit">Search</button>
                    </form>
                    <div id="search-results" class="search-results"></div>
                </div>
                
                <div class="section">
                    <h2>Available API Endpoints:</h2>
                    <div class="api-endpoint">
                        <code>GET /search/&lt;topic&gt;</code> - Search books by topic
                    </div>
                    <div class="api-endpoint">
                        <code>GET /info/&lt;item_number&gt;</code> - Get detailed information about a book
                    </div>
                    <div class="api-endpoint">
                        <code>POST /purchase/&lt;item_number&gt;</code> - Purchase a book
                    </div>
                </div>
                <div class="section">
                    <h2>Available Topics:</h2>
                    <ul>
                        <li>distributed systems</li>
                        <li>undergraduate school</li>
                    </ul>
                </div>
                <div class="section">
                    <h2>Available Books:</h2>
                    <ul>
                        <li>1 - How to get a good grade in DOS in 40 minutes a day</li>
                        <li>2 - RPCs for Noobs</li>
                        <li>3 - Xen and the Art of Surviving Undergraduate School</li>
                        <li>4 - Cooking for the Impatient Undergrad</li>
                    </ul>
                </div>
            </div>
        </body>
    </html>
    """


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)