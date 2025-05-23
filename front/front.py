import requests

CATALOG_SERVER_URL = "http://catalog:5001"
ORDER_SERVER_URL = "http://order:5002"


def handle_search(topic):
    url = f"/search/{topic}"
    print(f"Sending search request: {url}")
    try:
        res = requests.get(CATALOG_SERVER_URL + url)
        print("Response:", res.json())
    except Exception as e:
        print("Error:", e)


def handle_info(item_number):
    url = f"/info/{item_number}"
    print(f"Sending info request: {url}")
    try:
        res = requests.get(CATALOG_SERVER_URL + url)
        print("Response:", res.json())
    except Exception as e:
        print("Error:", e)


def handle_purchase(item_number):
    url = 'http://order:5002/purchase'
    payload = {"item_number": item_number}
    print(f"[FRONTEND] Sending purchase request to {url} with payload {payload}")
    try:
        response = requests.post(url, json=payload)
        print(response.json())
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
