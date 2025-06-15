from flask import Flask, request, jsonify
from datetime import datetime
import os
import requests

app = Flask(__name__)
ORDERS_FILE = "orders.log"


@app.route("/purchase", methods=["POST"])
def purchase():
    data = request.get_json()
    item_number = data["item_number"]
    print(f"[ORDER] Received purchase request: {data}")

    try:
        CATALOG_URL = os.getenv("CATALOG_URL", "http://catalog:5001")
        resp = requests.post(f"{CATALOG_URL}/decrease_stock/{item_number}")

        result = resp.json()
        print(f"[ORDER] Stock update response: {result}")

        if resp.status_code != 200 or result.get("status") != "success":
            return (
                jsonify(
                    {
                        "status": "fail",
                        "message": result.get("message", "Unknown error"),
                    }
                ),
                400,
            )

    except requests.exceptions.RequestException as e:
        print("Error updating stock:", e)
        return jsonify({"status": "fail", "message": "Stock update failed"}), 500

    # Log order if stock update was successful
    with open(ORDERS_FILE, "a") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - Purchased item {item_number}\n")

    return jsonify({"status": "success", "message": "Order placed"}), 200

@app.route("/admin_update/<int:item_number>", methods=["POST"])

def admin_update(item_number):
    data = request.get_json()
    print(f"[ORDER] Received admin update for item {item_number}: {data}")

    try:
        CATALOG_URL = os.getenv("CATALOG_URL", "http://catalog:5001")
        resp = requests.post(f"{CATALOG_URL}/update/{item_number}", json=data)
        result = resp.json()
        print(f"[ORDER] Forwarded to catalog, response: {result}")
        return jsonify(result), resp.status_code

    except requests.exceptions.RequestException as e:
        print("Error forwarding admin update to catalog:", e)
        return jsonify({"status": "fail", "message": "Catalog update failed"}), 500



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5002)

