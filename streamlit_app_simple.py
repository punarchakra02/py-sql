import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="E-Commerce Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stSelectbox {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Database connection function
@st.cache_resource
def get_database_connection():
    """Establish database connection with caching"""
    try:
        # Try to use Streamlit secrets first (for cloud deployment)
        if hasattr(st, 'secrets') and 'mysql' in st.secrets:
            conn = mysql.connector.connect(
                host=st.secrets.mysql.host,
                user=st.secrets.mysql.user,
                password=st.secrets.mysql.password,
                database=st.secrets.mysql.database,
                autocommit=True
            )
        else:
            # Use local MySQL (for local development)
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Punarbasu_03',
                database='ECOM',
                autocommit=True
            )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database connection failed: {err}")
        st.info("💡 **Tip**: Make sure your MySQL server is running and credentials are correct.")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

# Function to execute queries with error handling
def execute_query(query, connection):
    """Execute SQL query and return results"""
    try:
        if connection is None:
            st.error("No database connection available")
            return None
        
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except mysql.connector.Error as err:
        st.error(f"Query execution failed: {err}")
        return None
    except Exception as e:
        st.error(f"Unexpected error during query execution: {e}")
        return None

# Main app
def main():
    st.title("🛒 E-Commerce Data Analysis Dashboard")
    st.markdown("---")
    
    # Get database connection
    db_connection = get_database_connection()
    
    if db_connection is None:
        st.error("❌ Unable to connect to database. Please check your connection settings.")
        st.info("📝 **Note**: This app requires a MySQL database connection. Make sure your database is running.")
        if st.button("🔄 Try Reconnecting"):
            st.cache_resource.clear()
            st.rerun()
        return
    
    st.success("✅ Connected to database successfully!")
    
    # Sidebar navigation
    st.sidebar.title("📋 Navigation")
    analysis_type = st.sidebar.selectbox(
        "Choose Analysis Type:",
        [
            "📊 Overview",
            "🏙️ Customer Analysis", 
            "📦 Order Analysis",
            "💰 Sales & Revenue",
            "📈 Time Series Analysis",
        ]
    )
    
    if analysis_type == "📊 Overview":
        st.header("Dashboard Overview")
        
        # Key Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Total customers
            query = "SELECT COUNT(DISTINCT customer_id) as total_customers FROM customers"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Total Customers", f"{result[0][0]:,}")
        
        with col2:
            # Total orders
            query = "SELECT COUNT(DISTINCT order_id) as total_orders FROM orders"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Total Orders", f"{result[0][0]:,}")
        
        with col3:
            # Total revenue
            query = "SELECT ROUND(SUM(payment_value), 2) as total_revenue FROM payments"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Total Revenue", f"${result[0][0]:,.2f}")
        
        st.markdown("---")
        st.markdown("### 📋 About This Dashboard")
        st.markdown("This dashboard analyzes e-commerce data including:")
        st.markdown("• **Customer Demographics**: Cities, states, and customer distribution")
        st.markdown("• **Order Patterns**: Monthly trends, seasonal analysis")
        st.markdown("• **Sales Performance**: Category-wise sales, revenue analysis") 
        st.markdown("• **Business Metrics**: Growth rates, retention, top performers")
        st.markdown("Navigate through different sections using the sidebar to explore various aspects of the data.")
    
    elif analysis_type == "🏙️ Customer Analysis":
        st.header("Customer Analysis")
        
        # Customer distribution by state
        query = """
        SELECT customer_state, COUNT(*) as customer_count
        FROM customers
        GROUP BY customer_state
        ORDER BY customer_count DESC
        LIMIT 10
        """
        result = execute_query(query, db_connection)
        
        if result:
            df = pd.DataFrame(result, columns=['State', 'Customer Count'])
            
            fig = px.bar(df, x='State', y='Customer Count', 
                        title="Top 10 States by Customer Count")
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df)
    
    elif analysis_type == "📦 Order Analysis":
        st.header("Order Analysis")
        
        # Orders by month
        query = """
        SELECT 
            DATE_FORMAT(order_purchase_timestamp, '%Y-%m') as month,
            COUNT(*) as order_count
        FROM orders
        GROUP BY DATE_FORMAT(order_purchase_timestamp, '%Y-%m')
        ORDER BY month
        """
        result = execute_query(query, db_connection)
        
        if result:
            df = pd.DataFrame(result, columns=['Month', 'Order Count'])
            
            fig = px.line(df, x='Month', y='Order Count', 
                         title="Orders Over Time")
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df)
    
    elif analysis_type == "💰 Sales & Revenue":
        st.header("Sales & Revenue Analysis")
        
        # Revenue by product category
        query = """
        SELECT 
            p.product_category as category,
            ROUND(SUM(pay.payment_value), 2) as total_revenue
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN payments pay ON oi.order_id = pay.order_id
        GROUP BY p.product_category
        ORDER BY total_revenue DESC
        LIMIT 10
        """
        result = execute_query(query, db_connection)
        
        if result:
            df = pd.DataFrame(result, columns=['Category', 'Revenue'])
            
            fig = px.bar(df, x='Category', y='Revenue',
                        title="Revenue by Product Category")
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df)
    
    elif analysis_type == "📈 Time Series Analysis":
        st.header("Time Series Analysis")
        
        # Monthly revenue trend
        query = """
        SELECT 
            DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') as month,
            ROUND(SUM(p.payment_value), 2) as monthly_revenue
        FROM orders o
        JOIN payments p ON o.order_id = p.order_id
        GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
        ORDER BY month
        """
        result = execute_query(query, db_connection)
        
        if result:
            df = pd.DataFrame(result, columns=['Month', 'Revenue'])
            
            fig = px.line(df, x='Month', y='Revenue',
                         title="Monthly Revenue Trend")
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df)
    
    # Footer
    st.markdown("---")
    st.markdown("### 📊 Dashboard created using Streamlit")
    st.markdown("*Data source: E-commerce MySQL Database*")
    
    # Professional Links Section
    st.markdown("---")
    st.markdown("### 👨‍💻 Created by Punarbasu Chakraborty")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("🔗 **LinkedIn**")
        st.markdown("[Connect with me](https://linkedin.com/in/punarbasu-chakraborty-628566252)")
    
    with col2:
        st.markdown("🐙 **GitHub**")
        st.markdown("[View my projects](https://github.com/punarchakra02)")
    
    with col3:
        st.markdown("📧 **Email**")
        st.markdown("[Contact me](mailto:punarbasu02chakra@gmail.com)")
    
    st.markdown("---")
    st.markdown("*Built with ❤️ using Python, SQL & Streamlit*")

if __name__ == "__main__":
    main()
