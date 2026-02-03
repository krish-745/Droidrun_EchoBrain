---
name: shop-manager
description: Manage the SQLite database at C:\Users\krish\OneDrive\Documents\droidrun\brain.db. This skill provides tools to add products, list orders (all and active), and list customer queries (all and unresolved). Use this skill when managing shop inventory, orders, and customer queries within the specified SQLite database.
---

# Shop Manager

## Overview

This skill enables interaction with the shop's SQLite database located at `C:\Users\krish\OneDrive\Documents\droidrun\brain.db` to manage products, orders, and customer queries.

## Tools

This skill provides the following tools, implemented as Python scripts in the `scripts/` directory:

### 1. `add_product`

**Description:** Adds a new product to the `products` table in the database.
**Usage:** `python scripts/add_product.py <name> <price> <info>`
**Arguments:**
- `name`: The name of the product (e.g., "Classic Denim Jacket")
- `price`: The price of the product (e.g., "2500 INR")
- `info`: Additional information about the product (e.g., "Oversized fit, 100% cotton")
**Output:** Prints "✅ Added product" on success, or an error message if it fails.

### 2. `list_all_orders`

**Description:** Lists all orders from the `orders` table, indicating whether they are completed or pending.
**Usage:** `python scripts/list_all_orders.py`
**Output:** For each order, prints its status (✅ Completed or ⏳ Pending), Order ID, and Description.

### 3. `list_active_orders`

**Description:** Lists only the pending orders from the `orders` table.
**Usage:** `python scripts/list_active_orders.py`
**Output:** Prints "(Pending) PENDING ORDERS:" followed by the Order ID and Description for each pending order.

### 4. `list_all_queries`

**Description:** Lists all customer queries from the `queries` table, indicating whether they are resolved or pending.
**Usage:** `python scripts/list_all_queries.py`
**Output:** For each query, prints its status ((Resolved or Pending)), Query ID, Customer, and Info.

### 5. `list_active_queries`

**Description:** Lists only the unresolved customer queries from the `queries` table.
**Usage:** `python scripts/list_active_queries.py`
**Output:** Prints "(Pending) UNRESOLVED QUERIES:" followed by the Query ID, Customer, and Info for each unresolved query.

### 6. `list_all_products`

**Description:** Lists all products from the `products` table, including their names, prices, and information.
**Usage:** `python scripts/list_all_products.py`
**Output:** Prints "--- ALL PRODUCTS ---" followed by the Product ID, Name, Price, and Info for each product.

### 7. `resolve_query`

**Description:** Marks a specific customer query as resolved by updating its `completed` status to `1`.
**Usage:** `python scripts/resolve_query.py <query_id>`
**Arguments:**
- `query_id`: The ID of the query to resolve.
**Output:** Prints "(Completed) Query ID <query_id> marked as resolved." on success, or an error message.

### 8. `complete_order`

**Description:** Marks a specific order as completed by updating its `completed` status to `1`.
**Usage:** `python scripts/complete_order.py <order_id>`
**Arguments:**
- `order_id`: The ID of the order to complete.
**Output:** Prints "(Completed) Order ID <order_id> marked as completed." on success, or an error message.

### 9. `remove_product`

**Description:** Removes a product from the `products` table using its `product_id`.
**Usage:** `python scripts/remove_product.py <product_id>`
**Arguments:**
- `product_id`: The ID of the product to remove.
**Output:** Prints "(Completed) Product ID <product_id> removed successfully." on success, or an error message.

---

## Database Schema

For these scripts to work, the database `C:\Users\krish\OneDrive\Documents\droidrun\brain.db` is confirmed to have the following tables and columns:

### `orders` table:
- `customer` (TEXT)
- `description` (TEXT)
- `timestamp` (DATETIME DEFAULT CURRENT_TIMESTAMP)
- `product_id` (INTEGER)
- `order_id` (INTEGER, PRIMARY KEY AUTOINCREMENT)
- `completed` (INTEGER DEFAULT 0)

### `owner` table:
- `name` (TEXT)
- `mobile_number` (INTEGER UNIQUE)

### `products` table:
- `name` (TEXT)
- `price` (TEXT)
- `info` (TEXT)
- `product_id` (INTEGER, PRIMARY KEY AUTOINCREMENT)

### `queries` table:
- `query_id` (INTEGER, PRIMARY KEY AUTOINCREMENT)
- `customer` (TEXT)
- `timestamp` (DATETIME DEFAULT CURRENT_TIMESTAMP)
- `type` (TEXT)
- `info` (TEXT)
- `completed` (INTEGER DEFAULT 0)
