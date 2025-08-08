import sqlite3

conn = sqlite3.connect('reviews.db')
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS product_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    review TEXT
)
""")

# Sample data
c.executemany("""
INSERT INTO product_reviews (product_name, review) VALUES (?, ?)
""", [
    ('iPhone 15', 'The camera is excellent!'),
    ('iPhone 15', 'Battery life is just okay.'),
    ('iPhone 15', 'Beautiful screen but expensive.'),
    ('Pixel 8', 'Display is super vibrant and crisp.'),
    ('Pixel 8', 'Great value for the price.'),
])

conn.commit()
conn.close()
