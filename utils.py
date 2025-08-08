import pandas as pd

def load_reviews_from_csv(file):
    df = pd.read_csv(file)
    # Try to be smart about the likely review column
    review_col = next((col for col in df.columns if "review" in col.lower()), df.columns[0])
    return df[review_col].astype(str).tolist()

import sqlite3

def load_reviews_from_db(table_name, product_name=None, db_path="reviews.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    if product_name:
        c.execute(f"SELECT review FROM {table_name} WHERE product_name=?", (product_name,))
    else:
        c.execute(f"SELECT review FROM {table_name}")
    results = c.fetchall()
    conn.close()
    return [r[0] for r in results]

import sqlite3

def get_unique_products(table_name="product_reviews", db_path="reviews.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f"SELECT DISTINCT product_name FROM {table_name}")
    products = [row[0] for row in c.fetchall()]
    conn.close()
    return products
