# 🛒 Bazar Microservices

A containerized microservices-based online bookstore system built with **Flask** and **Docker**, demonstrating service-oriented architecture with independent services for catalog management, order processing, and administration.

> 📚 **University Project** — Advanced Software Engineering Course | An-Najah National University

---

## 🎯 Project Overview

Bazar is a distributed bookstore application split into independent microservices, each running in its own Docker container. The system demonstrates key microservices concepts including service decomposition, inter-service communication, containerization, and orchestration.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                 Docker Compose                  │
│                                                 │
│  ┌─────────────┐  ┌──────────┐  ┌─────────────┐ │
│  │   Catalog   │  │  Order   │  │    Admin    │ │
│  │   Service   │  │ Service  │  │  Dashboard  │ │
│  │  (Flask)    │  │ (Flask)  │  │  (Flask)    │ │
│  │  Port 500   │  │ Port 5002│  │  Port 5003  │ │
│  └─────────────┘  └──────────┘  └─────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Services

| Service | Description | Port |
|---------|-------------|------|
| **Catalog** | Product management — browse, search, and manage book inventory | 5001 |
| **Order** | Order processing — place and track book orders | 5002 |
| **Admin** | Dashboard — admin interface for managing the system | 5003 |

---

## 💻 Tech Stack

- **Backend:** Python, Flask
- **Containerization:** Docker, Docker Compose
- **API:** REST APIs for inter-service communication
- **Frontend:** HTML/CSS (Admin Dashboard)

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose installed

### Run the Application

```bash
# Clone the repository
git clone https://github.com/Mohamad-Salha/Bazar-Microservices.git
cd Bazar-Microservices

# Start all services
docker-compose up --build

# Services will be available at:
# Catalog: http://localhost:5001
# Order:   http://localhost:5002
# Admin:   http://localhost:5003
```

### Stop the Application

```bash
docker-compose down
```

---

## 📁 Project Structure

```
Bazar-Microservices/
├── catalog/          # Catalog microservice
├── order/            # Order microservice
├── admin/            # Admin dashboard
├── front/            # Frontend assets
├── docker-compose.yml
├── LICENSE
└── README.md
```

---

## ✨ Key Features

- ✅ **Service Decomposition** — Each service handles a single responsibility
- ✅ **Containerized** — Each service runs in its own Docker container
- ✅ **Docker Compose Orchestration** — One command to spin up the entire system
- ✅ **REST APIs** — Services communicate via HTTP REST endpoints
- ✅ **Admin Dashboard** — Web interface for system management

---

## 📧 Contact

**Mohamad Salha**
- 📧 mohamadsalha88@gmail.com
- 🔗 [LinkedIn](https://www.linkedin.com/in/mohamad-salha88)
- 💻 [GitHub](https://github.com/Mohamad-Salha)

---

**License:** MIT
