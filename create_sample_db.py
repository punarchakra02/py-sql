"""
Database creation script for Streamlit Cloud deployment
Creates SQLite database from sample data if no database exists
"""

import sqlite3
import pandas as pd
import streamlit as st
import os

def create_sample_database():
    """Create a sample SQLite database for demonstration purposes"""
    if os.path.exists("ecom.db"):
        return  # Database already exists
    
    st.info("🏗️ Creating sample database for demonstration...")
    
    # Create SQLite connection
    conn = sqlite3.connect("ecom.db")
    
    # Create sample data (much smaller than full dataset)
    
    # Sample customers data
    customers_data = {
        'customer_id': [f'customer_{i}' for i in range(1, 1001)],
        'customer_city': ['Sao Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Brasilia', 'Curitiba'] * 200,
        'customer_state': ['SP', 'RJ', 'MG', 'DF', 'PR'] * 200
    }
    customers_df = pd.DataFrame(customers_data)
    customers_df.to_sql('customers', conn, if_exists='replace', index=False)
    
    # Sample orders data
    orders_data = {
        'order_id': [f'order_{i}' for i in range(1, 1001)],
        'customer_id': [f'customer_{i}' for i in range(1, 1001)],
        'order_purchase_timestamp': pd.date_range('2017-01-01', periods=1000, freq='D')
    }
    orders_df = pd.DataFrame(orders_data)
    orders_df.to_sql('orders', conn, if_exists='replace', index=False)
    
    # Sample products data
    products_data = {
        'product_id': [f'product_{i}' for i in range(1, 501)],
        'product_category': ['electronics', 'clothing', 'books', 'home', 'sports'] * 100
    }
    products_df = pd.DataFrame(products_data)
    products_df.to_sql('products', conn, if_exists='replace', index=False)
    
    # Sample payments data
    payments_data = {
        'order_id': [f'order_{i}' for i in range(1, 1001)],
        'payment_value': [round(50 + (i % 200), 2) for i in range(1000)],
        'payment_installments': [1, 2, 3, 4, 5] * 200
    }
    payments_df = pd.DataFrame(payments_data)
    payments_df.to_sql('payments', conn, if_exists='replace', index=False)
    
    # Sample order_items data
    order_items_data = {
        'order_id': [f'order_{i}' for i in range(1, 1001)],
        'product_id': [f'product_{(i % 500) + 1}' for i in range(1000)],
        'seller_id': [f'seller_{(i % 100) + 1}' for i in range(1000)],
        'price': [round(30 + (i % 150), 2) for i in range(1000)]
    }
    order_items_df = pd.DataFrame(order_items_data)
    order_items_df.to_sql('order_items', conn, if_exists='replace', index=False)
    
    # Sample sellers data
    sellers_data = {
        'seller_id': [f'seller_{i}' for i in range(1, 101)],
        'seller_city': ['Sao Paulo', 'Rio de Janeiro', 'Belo Horizonte'] * 34,
        'seller_state': ['SP', 'RJ', 'MG'] * 34
    }
    sellers_df = pd.DataFrame(sellers_data[:100])  # Take only first 100
    sellers_df.to_sql('sellers', conn, if_exists='replace', index=False)
    
    # Sample geolocation data
    geolocation_data = {
        'geolocation_zip_code_prefix': [f'0{i:04d}' for i in range(1000)],
        'geolocation_lat': [-23.5 + (i * 0.01) for i in range(1000)],
        'geolocation_lng': [-46.6 + (i * 0.01) for i in range(1000)],
        'geolocation_city': ['Sao Paulo'] * 1000,
        'geolocation_state': ['SP'] * 1000
    }
    geolocation_df = pd.DataFrame(geolocation_data)
    geolocation_df.to_sql('geolocation', conn, if_exists='replace', index=False)
    
    conn.close()
    st.success("✅ Sample database created successfully!")

if __name__ == "__main__":
    create_sample_database()
    print("Sample database created!")
