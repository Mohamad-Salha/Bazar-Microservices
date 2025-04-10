from flask import Flask, request, jsonify
import requests
#frontend
app = Flask(__name__)

CATALOG_SERVER = "http://catalog:5001"
ORDER_SERVER = "http://order:5002"


@app.route('/search', methods=['GET'])
def search():
    topic = request.args.get('topic')
    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    # Send request to the catalog service
    response = requests.get(f"{CATALOG_SERVER}/search?topic={topic}")

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Log the response data for debugging (optional)
        print(f"Response from Catalog Service: {response.json()}")
        # Return the response to the frontend
        return jsonify(response.json())
    else:
        # Handle errors if the catalog service response is not successful
        print(f"Error from Catalog Service: {response.text}")
        return jsonify({"error": "Failed to fetch data from catalog service"}), 500


@app.route('/info/<item_number>', methods=['GET'])
def info(item_number):
    response = requests.get(f"{CATALOG_SERVER}/info/{item_number}")
    return jsonify(response.json())

@app.route('/purchase/<item_number>', methods=['POST'])
def purchase(item_number):
    response = requests.post(f"{ORDER_SERVER}/purchase/{item_number}")
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
