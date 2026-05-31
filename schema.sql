CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    category TEXT,
    part_type TEXT NOT NULL DEFAULT 'OEM' CHECK(part_type IN ('OEM', 'Aftermarket')),
    brand TEXT,
    serial_number INTEGER,
    price REAL DEFAULT 0.0,
    low_stock_threshold INTEGER NOT NULL DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
    UNIQUE(user_id, name)
);