# 🛒 KK Clothes - Retail ERP & Inventory Billing System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite)
![Status](https://img.shields.io/badge/Status-Completed-success)

A modern, lightweight retail ERP, Point-of-Sale (POS), and inventory management system built with **Python, FastAPI, SQLite, and Jinja2**. Designed specifically for apparel retailers to track stock levels, eliminate duplicate stock entries, automate real-time profit analytics, and export business audit reports to Excel/CSV.

---

## 🌟 Key Features

- **Full CRUD Inventory Management:** Add, view, update, and delete clothing products.
- **Smart Duplicate Prevention & Auto-Merge:** Adding an existing item automatically increments existing stock rather than creating redundant database records.
- **1-Click Restock & Sell Operations:** Instant stock deductions and increments without full page refreshes.
- **Dynamic Search & Multi-Category Filtering:** Real-time search by apparel title and category-based filtering (Men's Wear, Women's Wear, Kids Wear).
- **Real-Time Financial Analytics:** Instant calculation of Total Invested Capital, Total Sales Count, and Net Profit (`profit = selling_price - cost_price`).
- **Low Stock & Sold-Out Visual Indicators:** Automated dynamic visual badges triggering when stock drops below 3 units.
- **Audit-Ready Sales History:** Detailed transaction log tracking individual product sales, profit margins, and timestamps (`sold_at`).
- **Memory-Optimized CSV Exports:** Instant streaming export for both Current Inventory and Sales Audit logs to Excel/CSV using Python's `StreamingResponse`.
- **Fully Responsive Modern UI:** Built with custom CSS Grid & Flexbox, featuring mobile horizontal table scrolling and adaptive layouts.

---

## 🗄️ Database Schema

### 1. `products` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique product identifier |
| `item_name` | TEXT | NOT NULL | Title of the garment |
| `category` | TEXT | NOT NULL | Wear category (Men's, Women's, Kids) |
| `size` | TEXT | NOT NULL | Garment size (S, M, L, XL, etc.) |
| `cost_price` | REAL | NOT NULL | Purchase cost price (INR) |
| `selling_price` | REAL | NOT NULL | Retail selling price (INR) |
| `quantity` | INTEGER | NOT NULL | Available inventory quantity |

### 2. `sales` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique transaction receipt ID |
| `product_id` | INTEGER | NULLABLE | Linked reference to original product |
| `item_name` | TEXT | NOT NULL | Product name at time of sale |
| `cost_price` | REAL | NOT NULL | Cost price at time of sale |
| `selling_price` | REAL | NOT NULL | Final sold price |
| `profit` | REAL | NOT NULL | Net profit (`selling_price - cost_price`) |
| `sold_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Transaction datetime stamp |

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/KrishnaHagari/KKclothes.git](https://github.com/KrishnaHagari/KKclothes.git)
   cd KKclothes