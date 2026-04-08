# 🍔Restaurant Management System (CLI)

A simple, internal restaurant management application built with **Python** With class-based and **PostgreSQL**. Designed for restaurant managers and waiters. 



## 🔥 Features
### 🚀 This program automatically creates the database and tables — so you don't need to know SQL or write any queries.😎
### 🪑 Table Management
- Add / remove tables
- Update table status (available / occupied)
- View all tables in a clean formatted view

### 📋 Menu Management
- Full CRUD operations for menu items
- Add new dishes 🍕
- Edit prices
- Remove outdated items

### 🛒 Order Handling
- Create new orders
- Add items with quantities
- Update order status (received → paid)
- View detailed order breakdown

### 📊 Reporting
- Daily sales summary
- Subtotals and total revenue
- List of unpaid orders

### ✅ Input Validation
- Prevents invalid data (e.g., negative prices, empty inputs)

### 📝 Logging
- Errors stored in `app.log` for debugging

---

## 🛠️ Prerequisites

- Python 3.8+
- PostgreSQL (local or cloud)
- Required libraries:
  - psycopg2
  - tabulate
  - python-dotenv

---

## 🚀 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/restaurant-management-system.git
cd restaurant-management-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Linux / macOS:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install psycopg2 tabulate python-dotenv
```

### 4️⃣ Configure Environment Variables

Create a `.env` file based on `.env.example`:

```env
DB_NAME=restaurant_db
DB_USERNAME=youruser
DB_PASSWORD=yourpass
DB_HOST=localhost
DB_PORT=5432
```

## ⚙️ Database Setup

1.  Create a PostgreSQL database named `restaurant_db`.
2.  Create the required tables (`menu_items`, `tables`, `orders`, `order_details`) in your database.
3.  Update the `get_connection()` function in `app.py` with your database credentials (user, password, host).

## ▶️ How to Run

Run the script directly from your terminal:

```bash
python app.py
```
<b>😎 New features and improvements are on the way! 
  😅😄😘</b>
</p>


Developed by [Ehsan Barghamadi](https://github.com/EhsanBarghamadi)