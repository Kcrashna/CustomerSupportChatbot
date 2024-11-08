"""
database.py
This module provides functions to interact with an SQLite database for a knowledge base. It includes functionality to create tables, insert data, and retrieve information. Additionally, it supports logging purchase history and recommending products based on user purchase history.
Functions:
    connect_db():
        Connect to the SQLite database (or create it if it doesn't exist).
    create_tables():
        Creates tables for the knowledge base.
    insert_product(name, description):
        Insert product information into the products table.
    insert_faq(question, answer):
        Insert FAQ into the faqs table.
    get_product_info(name):
        Retrieve product information based on name.
    get_faq_answer(question):
        Retrieve answer for a FAQ based on the question.
    create_purchase_history_table():
        Creates a table for purchase history.
    log_purchase(user_id, product_id):
        Log a purchase in the purchase history table.
    recommend_products(user_id):
        Recommend products to a user based on their purchase history.
"""
import sqlite3
def connect_db():
    """Connect to the SQLite database (or create it if it doesn't exist)."""
    conn = sqlite3.connect('knowledge_base.db')
    return conn

def create_tables():
    """Creates tables for the knowledge base."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        description TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS faqs (
        id INTEGER PRIMARY KEY,
        question TEXT UNIQUE,
        answer TEXT
    )
    ''')
    conn.commit()
    conn.close()

def insert_product(name, description):
    """Insert product information into the products table."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO products (name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    conn.close()

def insert_faq(question, answer):
    """Insert FAQ into the faqs table."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO faqs (question, answer) VALUES (?, ?)', (question, answer))
    conn.commit()
    conn.close()

def get_product_info(name):
    """Retrieve product information based on name."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT description FROM products WHERE name = ?', (name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Product not found."

def get_faq_answer(question):
    """Retrieve answer for a FAQ based on the question."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT answer FROM faqs WHERE question = ?', (question,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "FAQ not found."

'''Adding a table for purchase history and necessary functions to log purchases and fetch recommendations.'''
def create_purchase_history_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS purchase_history (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        product_id INTEGER,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')
    conn.commit()
    conn.close()

'''This function will log a purchase in the purchase history table.'''
def log_purchase(user_id, product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO purchase_history (user_id, product_id) VALUES (?, ?)', (user_id, product_id))
    conn.commit()
    conn.close()

'''This function will recommend products to a user based on their purchase history.'''
def recommend_products(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT name FROM products WHERE id IN
                      (SELECT product_id FROM purchase_history WHERE user_id = ?)''', (user_id,))
    recommendations = cursor.fetchall()
    conn.close()
    return [rec[0] for rec in recommendations] if recommendations else ["No recommendations available."]

