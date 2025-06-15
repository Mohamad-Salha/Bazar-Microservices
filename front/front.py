import requests
import time
import os

# Backends
CATALOG_SERVERS = ["http://catalog1:5001", "http://catalog2:5001"]
ORDER_SERVERS = ["http://order1:5002", "http://order2:5002"]
catalog_index = 0
order_index = 0

# Cache settings
cache = {}
CACHE_TTL_SECONDS = 30

def get_next_catalog_url():
    global catalog_index
    url = CATALOG_SERVERS[catalog_index]
    catalog_index = (catalog_index + 1) % len(CATALOG_SERVERS)
    return url

def get_next_order_url():
    global order_index
    url = ORDER_SERVERS[order_index]
    order_index = (order_index + 1) % len(ORDER_SERVERS)
    return url

def get_from_cache_or_fetch(key, url):
    current_time = time.time()
    if key in cache:
        entry = cache[key]
        if current_time - entry["timestamp"] < CACHE_TTL_SECONDS:
            print(f"[CACHE] HIT for {key}")
            return entry["data"]
        else:
            print(f"[CACHE] EXPIRED for {key}")
            del cache[key]

    try:
        print(f"[CACHE] MISS - fetching {url}")
        res = requests.get(url)
        data = res.json()
        cache[key] = {"data": data, "timestamp": current_time}
        return data
    except Exception as e:
        print("Error fetching from catalog:", e)
        return {"error": str(e)}

def handle_search(topic):
    url = f"/search/{topic}"
    full_url = get_next_catalog_url() + url
    data = get_from_cache_or_fetch(url, full_url)
    print("Response:", data)

def handle_info(item_number):
    url = f"/info/{item_number}"
    full_url = get_next_catalog_url() + url
    data = get_from_cache_or_fetch(url, full_url)
    print("Response:", data)

def handle_purchase(item_number):
    url = get_next_order_url() + "/purchase"
    payload = {"item_number": item_number}
    print(f"[FRONTEND] Sending purchase request to {url} with payload {payload}")
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        print(data)

        # Invalidate cache for info of purchased item
        info_key = f"/info/{item_number}"
        if info_key in cache:
            del cache[info_key]
            print(f"[CACHE] Invalidated {info_key} due to purchase.")

    except requests.exceptions.RequestException as e:
        print("Error:", e)

def main():
    print("Welcome to Bazar.com CLI!")
    print(
        "Type a command: search <topic>, info <item_number>, purchase <item_number>, or exit"
    )

    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            break

        parts = user_input.split()
        if not parts:
            continue

        command = parts[0].lower()

        if command == "search" and len(parts) >= 2:
            topic = " ".join(parts[1:])
            handle_search(topic)
        elif command == "info" and len(parts) == 2 and parts[1].isdigit():
            handle_info(int(parts[1]))
        elif command == "purchase" and len(parts) == 2 and parts[1].isdigit():
            handle_purchase(int(parts[1]))
        else:
            print(
                "Invalid command. Try: search <topic>, info <item_number>, purchase <item_number>"
            )

if __name__ == "__main__":
    main()

