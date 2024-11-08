
"""
This script initializes the database with predefined tables and sample data.
Functions:
    initialize_database():
        Creates necessary tables and inserts sample data into the database.
        - Inserts sample products: 'laptop' and 'phone'.
        - Inserts sample FAQs.
        - Logs sample purchases for testing the recommendation system.
Usage:
    Run this script directly to initialize the database with sample data.
    Example:
        python initialize_db.py
"""
from database import create_tables, insert_product, insert_faq, create_purchase_history_table, log_purchase
def initialize_database():
    create_tables()
    insert_product('laptop', 'A high-performance laptop suitable for gaming and work.')
    insert_product('phone', 'A smartphone with advanced features and excellent camera.')
    insert_faq('What is the return policy?', 'You can return products within 30 days of purchase.')
    insert_faq('Do you offer warranty?', 'Yes, all products come with a one-year warranty.')
     # Log sample purchases for testing the recommendation system
    log_purchase('user1', 1)  # Assuming 'laptop' has product ID 1
    log_purchase('user1', 2)  # Assuming 'phone' has product ID 2

if __name__ == "__main__":
    initialize_database()
