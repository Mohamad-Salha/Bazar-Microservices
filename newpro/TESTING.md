# Testing Strategy for Bazar.com Microservices

This document outlines the testing strategy for the Bazar.com microservices application, which consists of three services:

1. **Catalog Service** - Manages book information and inventory
2. **Order Service** - Handles purchase orders and updates inventory
3. **Frontend Service** - Provides user interface and API endpoints

## Test Types

### Unit Tests

Unit tests verify the functionality of individual components in isolation:

- `test_catalog_service.py` - Tests the catalog service endpoints
- `test_order_service.py` - Tests the order service endpoints
- `test_frontend_service.py` - Tests the frontend service endpoints

These tests use mocking to isolate the service being tested from its dependencies.

### Integration Tests

`test_integration.py` tests the interaction between all three services to ensure they work together properly. It covers:

- Searching for books by topic
- Getting detailed book information
- The complete purchase flow
- Handling out-of-stock scenarios

## Running the Tests

### Running All Tests

To run all unit tests at once, use the test runner script:

```
python run_tests.py
```

### Running Integration Tests

To run the integration tests, make sure all three services are running (or let the test start them automatically):

```
python test_integration.py
```

### Running Individual Test Files

You can also run individual test files:

```
python test_catalog_service.py
python test_order_service.py
python test_frontend_service.py
```

## Test Coverage

The tests cover the following key functionality:

### Catalog Service
- Querying books by subject/topic
- Querying book details by item number
- Updating book details (stock or cost)

### Order Service
- Processing purchase orders
- Checking if books are in stock
- Decrementing stock when purchases are made
- Handling out-of-stock scenarios
- Handling errors when communicating with the catalog service

### Frontend Service
- Searching for books by topic
- Getting detailed book information
- Purchasing books
- Handling errors from backend services

### Integration
- End-to-end purchase flow
- Service communication
- Error handling across services

## Docker Testing

If you're using Docker, you can test the containerized services by:

1. Building the Docker images:
   ```
   docker build -f Dockerfile.catalog -t bazar-catalog .
   docker build -f Dockerfile.order -t bazar-order .
   docker build -f Dockerfile.frontend -t bazar-frontend .
   ```

2. Running the containers:
   ```
   docker run -d -p 5001:5001 --name catalog bazar-catalog
   docker run -d -p 5002:5002 --name order -e CATALOG_SERVICE_URL=http://catalog:5001 bazar-order
   docker run -d -p 5000:5000 --name frontend -e CATALOG_SERVICE_URL=http://catalog:5001 -e ORDER_SERVICE_URL=http://order:5002 bazar-frontend
   ```

3. Running the integration tests against the containerized services:
   ```
   python test_integration.py
   ```