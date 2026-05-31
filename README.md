# MechTrack — Mechanic Shop Inventory Tracker

A multi-user Flask web application for mechanic shops to manage and track parts inventory.

## Features

- **Authentication** — register, login, logout with hashed passwords
- **Parts Inventory** — full CRUD on parts with name, brand, category, type, serial number, price and quantity
- **Low Stock Alerts** — automatic flagging when parts fall below a set threshold
- **Audit Log** — tracks when each part was added and last updated
- **Search & Filter** — search by name or brand, filter by category and part type
- **Sort** — sort inventory by any column ascending or descending
- **Summary Stats** — total parts, units, categories and inventory value
- **Multi-user** — each mechanic sees only their own inventory

## Tech Stack

- **Backend** — Python, Flask, raw SQLite3 (no ORM)
- **Frontend** — Jinja2, HTML, CSS
- **Auth** — Flask sessions and cookies, Werkzeug password hashing
- **Testing** — Python unittest

## Project Structure