import requests

def update_item(item_number, stock=None, cost=None):
    data = {}
    if stock is not None:
        data["stock"] = stock
    if cost is not None:
        data["cost"] = cost

    try:
        resp = requests.post(f"http://order:5002/admin_update/{item_number}", json=data)
        print(f"[ADMIN] Response: {resp.status_code} - {resp.json()}")
    except requests.exceptions.RequestException as e:
        print(f"[ADMIN] Failed to update item: {e}")

def admin_cli():
    print("=== ADMIN MENU ===")
    while True:
        print("\n1. Update Stock")
        print("2. Update Cost")
        print("3. Update Both")
        print("0. Exit")

        choice = input("Enter choice: ").strip()
        if choice == "0":
            break

        try:
            item = int(input("Item number: "))
            stock = cost = None

            if choice == "1":
                stock = int(input("New stock: "))
            elif choice == "2":
                cost = int(input("New cost: "))
            elif choice == "3":
                stock = int(input("New stock: "))
                cost = int(input("New cost: "))
            else:
                print("Invalid choice.")
                continue

            update_item(item, stock, cost)

        except ValueError:
            print("Invalid input. Please enter numeric values.")

if __name__ == "__main__":
    admin_cli()
