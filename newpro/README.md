# Bazar.com - The World's Smallest Book Store

This project implements a two-tier microservice architecture for a small online bookstore called Bazar.com that sells only four books.

## Architecture

The system consists of three microservices:

1. **Front-end Service**: Handles user requests and performs initial processing
   - Endpoints: search, info, purchase

2. **Catalog Service**: Maintains the book catalog
   - Endpoints: query-by-subject, query-by-item, update

3. **Order Service**: Processes purchase orders
   - Endpoints: purchase

## Setup and Installation

### Prerequisites
- Python 3.8+
- Flask
- Requests library

### Installation

```bash
pip install flask requests
```

### Running the Services

Start each service in a separate terminal:

```bash
# Start Catalog Service
python catalog_service.py

# Start Order Service
python order_service.py

# Start Front-end Service
python frontend_service.py
```

## API Documentation

### Front-end Service

- `GET /search/<topic>` - Search books by topic
- `GET /info/<item_number>` - Get detailed information about a book
- `POST /purchase/<item_number>` - Purchase a book

### Catalog Service

- `GET /query/subject/<topic>` - Query books by subject/topic
- `GET /query/item/<item_number>` - Query book details by item number
- `PUT /update/<item_number>` - Update book details (stock or cost)

### Order Service

- `POST /purchase/<item_number>` - Process a purchase order

## Data Storage

The system uses simple CSV files for data persistence:
- `books.csv` - Stores the book catalog
- `orders.csv` - Stores the order history