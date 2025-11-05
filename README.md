# Sales Analytics API (Django REST Framework)

A fully functional **Sales Analytics API** built using **Django REST Framework**, featuring customer/product/order management, nested serializers, optimized analytics queries, and optional JWT authentication.

---

## ✅ Features

* Customer, Product, Order, OrderItem models
* Create orders with **nested items**
* Validations (quantity ≥ 1, order must have items)
* Annotated & optimized analytics queries
* Pagination enabled
* JWT Authentication (optional bonus)
* Date range filters for analytics
* Unit tests for an analytics endpoint

---

## ✅ Project Structure

```
sales_analytics/
│── manage.py
│
├── sales_analytics/             # project folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── api/                         # main app
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── admin.py
│
└── requirements.txt
```

---

## ✅ Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run Server

```bash
python manage.py runserver
```

---

## ✅ Available Endpoints

### **Customers**

| Method | Endpoint          | Description        |
| ------ | ----------------- | ------------------ |
| GET    | `/api/customers/` | List all customers |
| POST   | `/api/customers/` | Create customer    |

Example POST:

```json
{
  "name": "Suyash Dubey",
  "email": "suyash@example.com"
}
```

---

### **Products**

| Method | Endpoint         | Description       |
| ------ | ---------------- | ----------------- |
| GET    | `/api/products/` | List all products |
| POST   | `/api/products/` | Create product    |

Example POST:

```json
{
  "name": "Laptop",
  "price": "65000.00"
}
```

---

### **Orders (Nested)**

| Method | Endpoint       | Description             |
| ------ | -------------- | ----------------------- |
| GET    | `/api/orders/` | List orders with totals |
| POST   | `/api/orders/` | Create order & items    |

Example POST:

```json
{
    "customer": 1,
    "items": [
        {"product": 1, "quantity": 2},
        {"product": 3, "quantity": 1}
    ]
}
```

---

## ✅ Analytics Endpoints

### **1. Sales Summary**

`GET /api/analytics/sales-summary/?from=2024-01-01&to=2024-12-31`

Returns:

```json
{
  "total_sales": 120000,
  "total_customers": 10,
  "total_products_sold": 56
}
```

---

### **2. Top Customers**

`GET /api/analytics/top-customers/?from=2024-01-01&to=2024-12-31`

Returns:

```json
[
  { "customer": "Suyash", "amount": 45000 },
  { "customer": "Rahul", "amount": 30000 }
]
```

---

### **3. Top Products**

`GET /api/analytics/top-products/?from=2024-01-01&to=2024-12-31`

Returns:

```json
[
  { "product": "Phone", "sold": 25 },
  { "product": "Laptop", "sold": 14 }
]
```

---

## ✅ JWT Authentication (Bonus)

Enable JWT login:

```
/api/auth/login/
/api/auth/refresh/
```

Include in headers:

```
Authorization: Bearer <token>
```

---

## ✅ Running Tests

Run all tests:

```bash
python manage.py test
```

Example test included for:
✅ Top Products Analytics Endpoint

---

## ✅ Notes

* SQLite is default DB, works out of the box
* Pagination enabled (results key)
* All analytics functions optimized using annotate and select_related
* Orders cannot be empty
* OrderItem quantity must be ≥ 1

---

## ✅ Author

**Suyash Dubey**
Sales Analytics API — Fully functional DRF project.

---


