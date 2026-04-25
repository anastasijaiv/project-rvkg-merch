import sqlite3

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# ----------------------
# Create collections table
# ----------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS collections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    description TEXT
)
''')

# ----------------------
# Create products table
# ----------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    image_url TEXT NOT NULL,
    collection_id INTEGER,
    price DECIMAL(10,2),
    description TEXT,
    FOREIGN KEY(collection_id) REFERENCES collections(id)
)
''')

# ----------------------
# Create promo_codes table
# ----------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS promo_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    discount INTEGER NOT NULL,
    description TEXT
)
''')

conn.commit()
conn.close()
print("Tables created successfully!")
