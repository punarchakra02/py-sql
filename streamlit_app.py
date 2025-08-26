import streamlit as st
import pandas as pd
import seaborn as sns
import psycopg2
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import os
from urllib.parse import urlparse

# Set page config - PostgreSQL compatible version
st.set_page_config(
    page_title="E-Commerce Analysis Dashboard",
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
        # Check for NeonDB/PostgreSQL DATABASE_URL (priority for cloud deployment)
        if "DATABASE_URL" in st.secrets:
            DATABASE_URL=st.secrets["DATABASE_URL"]
        # else 'DATABASE_URL' in os.environ:
        #     database_url = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            conn.autocommit = True
            # st.success("🌐 Connected to NeonDB PostgreSQL database")
            return conn
        
        # Check for individual PostgreSQL environment variables
        elif all(key in os.environ for key in ['PGHOST', 'PGUSER', 'PGPASSWORD', 'PGDATABASE']):
            conn = psycopg2.connect(
                host=os.environ['PGHOST'],
                user=os.environ['PGUSER'],
                password=os.environ['PGPASSWORD'],
                database=os.environ['PGDATABASE'],
                port=os.environ.get('PGPORT', '5432'),
                sslmode='require'
            )
            conn.autocommit = True
            st.success("🌐 Connected to PostgreSQL database")
            return conn
        
        # Try to use Streamlit secrets (for Streamlit Cloud)
        elif hasattr(st, 'secrets') and 'connections' in st.secrets and 'neon' in st.secrets.connections:
            # Use NeonDB connection URL from secrets
            neon_url = st.secrets.connections.neon.url
            conn = psycopg2.connect(neon_url)
            conn.autocommit = True
            # st.success("🌐 Connected to NeonDB via connection URL")
            return conn
        
        # Try individual PostgreSQL secrets
        elif hasattr(st, 'secrets') and 'postgresql' in st.secrets:
            conn = psycopg2.connect(
                host=st.secrets.postgresql.host,
                user=st.secrets.postgresql.user,
                password=st.secrets.postgresql.password,
                database=st.secrets.postgresql.database,
                port=st.secrets.postgresql.get('port', '5432'),
                sslmode='require'
            )
            conn.autocommit = True
            st.success("☁️ Connected to Streamlit Cloud PostgreSQL database")
            return conn
        else:
            # Use local PostgreSQL (for local development)
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='Punarbasu_03',
                database='ECOM',
                port='5432'
            )
            conn.autocommit = True
            st.success("💻 Connected to local PostgreSQL database")
            return conn
    except psycopg2.Error as err:
        st.error(f"Database connection failed: {err}")
        st.info("**Tip**: Make sure your PostgreSQL server is running and credentials are correct.")
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
    except psycopg2.Error as err:
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
        st.info("📝 **Note**: This app requires a PostgreSQL database connection. Make sure your database is running.")
        if st.button("🔄 Try Reconnecting"):
            st.cache_resource.clear()
            st.rerun()
        return
    
    st.success("✅ Connected to database successfully!")
    
    # Sidebar navigation
    st.sidebar.title(" Navigation")
    analysis_type = st.sidebar.selectbox(
        "Choose Analysis Type:",
        [
            " Overview",
            " Customer Analysis", 
            " Order Analysis",
            " Sales & Revenue",
            " Time Series Analysis",
        ]
    )
    
    if analysis_type == " Overview":
        st.header("Dashboard Overview")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Total customers
            query = "SELECT COUNT(customer_id) as total_customers FROM customers"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Total Customers", f"{result[0][0]:,}")
        
        with col2:
            # Total unique orders
            query = "SELECT COUNT(DISTINCT order_id) as total_orders FROM orders"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Unique Orders", f"{result[0][0]:,}")
        
        with col3:
            # Total order records (including duplicates)
            query = "SELECT COUNT(*) as total_records FROM orders"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Order Records", f"{result[0][0]:,}")
        
        with col4:
            # Total revenue
            query = "SELECT ROUND(SUM(payment_value)::NUMERIC, 2) as total_revenue FROM payments"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Total Revenue", f"${result[0][0]:,.2f}")
        
        st.markdown("---")
        
        # Add data explanation
        st.info(" **Data Note**: 'Unique Orders' shows distinct business transactions, while 'Order Records' shows total database rows (including duplicates).")
        
        # Additional insights
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Customers with orders
            query = "SELECT COUNT(DISTINCT customer_id) FROM orders"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Active Customers", f"{result[0][0]:,}")
        
        with col_b:
            # Average order value
            query = "SELECT ROUND(AVG(payment_value)::NUMERIC, 2) FROM payments"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Avg Order Value", f"${result[0][0]:,.2f}")
        
        st.markdown("###  About This Dashboard")
        st.markdown("This dashboard analyzes e-commerce data including:")
        st.markdown("• **Customer Demographics**: Cities, states, and customer distribution")
        st.markdown("• **Order Patterns**: Monthly trends, seasonal analysis")
        st.markdown("• **Sales Performance**: Category-wise sales, revenue analysis") 
        st.markdown("• **Business Metrics**: Growth rates, retention, top performers")
        st.markdown("Navigate through different sections using the sidebar to explore various aspects of the data.")
    
    elif analysis_type == " Customer Analysis":
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
    
    elif analysis_type == " Order Analysis":
        st.header("Order Analysis")
        
        # Order statistics
        st.subheader("Order Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Unique orders
            query = "SELECT COUNT(DISTINCT order_id) as total_orders FROM orders"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Unique Orders", f"{result[0][0]:,}")
        
        with col2:
            # Orders per customer
            query = """
            SELECT ROUND((COUNT(DISTINCT order_id) * 1.0 / COUNT(DISTINCT customer_id))::NUMERIC, 2)
            FROM orders
            """
            result = execute_query(query, db_connection)
            if result:
                st.metric("Orders per Customer", f"{result[0][0]:.2f}")
        
        with col3:
            # Average order value
            query = "SELECT ROUND(AVG(payment_value)::NUMERIC, 2) FROM payments"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Avg Order Value", f"${result[0][0]:,.2f}")
        
        with col4:
            # Total products
            query = "SELECT COUNT(DISTINCT product_id) FROM products"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Total Products", f"{result[0][0]:,}")
        
        # Data quality metrics
        st.subheader(" Data Quality")
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Total order records
            query = "SELECT COUNT(*) FROM orders"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Order Records", f"{result[0][0]:,}")
        
        with col_b:
            # Duplicate factor
            query = """
            SELECT ROUND((COUNT(*) * 1.0 / COUNT(DISTINCT order_id))::NUMERIC, 1) as dup_factor 
            FROM orders
            """
            result = execute_query(query, db_connection)
            if result:
                st.metric("Duplicate Factor", f"{result[0][0]}x")
        
        st.info(" **Note**: Each order appears multiple times in the database. This could be due to order updates, multiple items, or data import issues.")
        
        # Orders by status
        st.subheader(" Orders by Status")
        query = "SELECT order_status, COUNT(DISTINCT order_id) as count FROM orders GROUP BY order_status ORDER BY count DESC"
        result = execute_query(query, db_connection)
        if result:
            df = pd.DataFrame(result, columns=['Status', 'Count'])
            fig = px.bar(df, x='Status', y='Count', title="Unique Orders by Status")
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Orders by month (using distinct orders to avoid duplicates)
        st.subheader("📅 Orders Over Time")
        query = """
        SELECT 
            TO_CHAR(order_purchase_timestamp::TIMESTAMP, 'YYYY-MM') as month,
            COUNT(DISTINCT order_id) as order_count
        FROM orders
        GROUP BY TO_CHAR(order_purchase_timestamp::TIMESTAMP, 'YYYY-MM')
        ORDER BY month
        """
        result = execute_query(query, db_connection)
        
        if result:
            df = pd.DataFrame(result, columns=['Month', 'Order Count'])
            
            fig = px.line(df, x='Month', y='Order Count', 
                         title="Unique Orders Over Time")
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == " Sales & Revenue":
        st.header("Sales & Revenue Analysis")
        
        # Revenue by product category
        query = """
        SELECT 
            p."product category" as category,
            ROUND(SUM(pay.payment_value)::NUMERIC, 2) as total_revenue
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN payments pay ON oi.order_id = pay.order_id
        GROUP BY p."product category"
        ORDER BY total_revenue DESC
        LIMIT 10
        """
        result = execute_query(query, db_connection)
        
        if result:
            df = pd.DataFrame(result, columns=['Category', 'Revenue'])
            
            fig = px.bar(df, x='Category', y='Revenue',
                        title="Revenue by Product Category")
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df)
    
    elif analysis_type == " Time Series Analysis":
        st.header("Time Series Analysis")
        
        # Monthly revenue trend (using distinct orders)
        query = """
        SELECT 
            TO_CHAR(o.order_purchase_timestamp::TIMESTAMP, 'YYYY-MM') as month,
            ROUND(SUM(p.payment_value)::NUMERIC, 2) as monthly_revenue,
            COUNT(DISTINCT o.order_id) as order_count
        FROM (SELECT DISTINCT order_id, order_purchase_timestamp FROM orders) o
        JOIN payments p ON o.order_id = p.order_id
        GROUP BY TO_CHAR(o.order_purchase_timestamp::TIMESTAMP, 'YYYY-MM')
        ORDER BY month
        """
        result = execute_query(query, db_connection)
        
        if result:
            df = pd.DataFrame(result, columns=['Month', 'Revenue', 'Order Count'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.line(df, x='Month', y='Revenue',
                             title="Monthly Revenue Trend")
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.line(df, x='Month', y='Order Count',
                             title="Monthly Order Count")
                st.plotly_chart(fig2, use_container_width=True)
            
            st.dataframe(df)
    
    # Footer
    st.markdown("---")
    st.markdown("### 📊 Dashboard created using Streamlit")
    st.markdown("*Data source: E-commerce PostgreSQL Database*")
    
    # Professional Links Section
    st.markdown("---")
    st.markdown("### 👨‍💻 Created by Punarbasu Chakraborty")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("🔗 **LinkedIn**")
        st.markdown("[Connect with me](https://linkedin.com/in/punarbasu-chakraborty-628566252/)")
    
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
