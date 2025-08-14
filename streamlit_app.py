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
                database=st.secrets.mysql.database
            )
        else:
            # Fallback to hardcoded values (for local development)
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Punarbasu_03',  # Note: In production, use environment variables
                database='ECOM'
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
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        st.error(f"Query execution failed: {err}")
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
            "🔄 Customer Retention",
            "🏆 Top Performers"
        ]
    )
    
    # Overview section
    if analysis_type == "📊 Overview":
        st.header("Dashboard Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Total customers
            query = "SELECT COUNT(DISTINCT customer_id) FROM customers"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Total Customers", f"{result[0][0]:,}")
        
        with col2:
            # Total orders
            query = "SELECT COUNT(order_id) FROM orders"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Total Orders", f"{result[0][0]:,}")
        
        with col3:
            # Total revenue
            query = "SELECT ROUND(SUM(payment_value), 2) FROM payments"
            result = execute_query(query, db_connection)
            if result:
                st.metric("Total Revenue", f"${result[0][0]:,.2f}")
        
        st.markdown("---")
        st.markdown("""
        ### 📋 About This Dashboard
        
        This dashboard analyzes e-commerce data including:
        - **Customer Demographics**: Cities, states, and customer distribution
        - **Order Patterns**: Monthly trends, seasonal analysis
        - **Sales Performance**: Category-wise sales, revenue analysis
        - **Business Metrics**: Growth rates, retention, top performers
        
        Navigate through different sections using the sidebar to explore various aspects of the data.
        """)
    
    # Customer Analysis
    elif analysis_type == "🏙️ Customer Analysis":
        st.header("Customer Analysis")
        
        tab1, tab2 = st.tabs(["Unique Cities", "Customers by State"])
        
        with tab1:
            st.subheader("Unique Customer Cities")
            query = "SELECT DISTINCT customer_city FROM customers ORDER BY customer_city"
            result = execute_query(query, db_connection)
            
            if result:
                df = pd.DataFrame(result, columns=["City"])
                st.write(f"**Total unique cities: {len(df)}**")
                st.dataframe(df, height=400)
        
        with tab2:
            st.subheader("Customer Distribution by State")
            query = """SELECT customer_state, COUNT(customer_id) as customer_count 
                      FROM customers GROUP BY customer_state ORDER BY customer_count DESC"""
            result = execute_query(query, db_connection)
            
            if result:
                df = pd.DataFrame(result, columns=["State", "Customer Count"])
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig = px.bar(df, x="State", y="Customer Count", 
                               title="Customers by State")
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.dataframe(df, height=400)
    
    # Order Analysis
    elif analysis_type == "📦 Order Analysis":
        st.header("Order Analysis")
        
        tab1, tab2, tab3 = st.tabs(["Orders by Year", "Monthly Orders 2018", "Average Products per Order"])
        
        with tab1:
            st.subheader("Orders by Year")
            year = st.selectbox("Select Year:", [2016, 2017, 2018])
            
            query = f"SELECT COUNT(order_id) FROM orders WHERE YEAR(order_purchase_timestamp) = {year}"
            result = execute_query(query, db_connection)
            
            if result:
                st.metric(f"Orders in {year}", f"{result[0][0]:,}")
        
        with tab2:
            st.subheader("Monthly Order Trends - 2018")
            query = """SELECT MONTHNAME(order_purchase_timestamp) AS month,
                             COUNT(*) AS orders
                      FROM orders
                      WHERE YEAR(order_purchase_timestamp) = 2018
                      GROUP BY MONTH(order_purchase_timestamp), MONTHNAME(order_purchase_timestamp)
                      ORDER BY MONTH(order_purchase_timestamp)"""
            
            result = execute_query(query, db_connection)
            
            if result:
                df = pd.DataFrame(result, columns=["Month", "Orders"])
                
                fig = px.line(df, x="Month", y="Orders", 
                            title="Monthly Orders in 2018", markers=True)
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(df)
        
        with tab3:
            st.subheader("Average Products per Order by City")
            query = """WITH count_per_order AS (
                        SELECT orders.order_id, orders.customer_id, 
                               COUNT(order_items.order_id) as product_count
                        FROM orders JOIN order_items ON orders.order_id = order_items.order_id
                        GROUP BY orders.order_id, orders.customer_id
                      ) 
                      SELECT customers.customer_city, 
                             ROUND(AVG(count_per_order.product_count), 2) as avg_products
                      FROM customers JOIN count_per_order 
                           ON customers.customer_id = count_per_order.customer_id
                      GROUP BY customers.customer_city
                      ORDER BY avg_products DESC
                      LIMIT 20"""
            
            result = execute_query(query, db_connection)
            
            if result:
                df = pd.DataFrame(result, columns=["City", "Average Products per Order"])
                
                fig = px.bar(df.head(10), x="City", y="Average Products per Order",
                           title="Top 10 Cities by Average Products per Order")
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(df)
    
    # Sales & Revenue Analysis
    elif analysis_type == "💰 Sales & Revenue":
        st.header("Sales & Revenue Analysis")
        
        tab1, tab2, tab3 = st.tabs(["Sales by Category", "Revenue Percentage", "Price vs Purchase Correlation"])
        
        with tab1:
            st.subheader("Total Sales by Product Category")
            query = """SELECT products.product_category as category, 
                             ROUND(SUM(payments.payment_value), 2) as sales 
                      FROM products JOIN order_items ON products.product_id = order_items.product_id
                      JOIN payments ON payments.order_id = order_items.order_id 
                      GROUP BY category
                      ORDER BY sales DESC"""
            
            result = execute_query(query, db_connection)
            
            if result:
                df = pd.DataFrame(result, columns=["Category", "Sales"])
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig = px.bar(df.head(15), x="Sales", y="Category", 
                               orientation='h', title="Top 15 Categories by Sales")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.dataframe(df.head(15))
        
        with tab2:
            st.subheader("Revenue Percentage by Category")
            query = """SELECT products.product_category as category, 
                             ROUND((SUM(payments.payment_value)/
                                   (SELECT SUM(payment_value) FROM payments))*100, 2) as sales_percentage
                      FROM products JOIN order_items ON products.product_id = order_items.product_id
                      JOIN payments ON payments.order_id = order_items.order_id
                      GROUP BY category 
                      ORDER BY sales_percentage DESC"""
            
            result = execute_query(query, db_connection)
            
            if result:
                df = pd.DataFrame(result, columns=["Category", "Percentage"])
                
                fig = px.pie(df.head(10), values="Percentage", names="Category",
                           title="Revenue Distribution by Top 10 Categories")
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(df.head(15))
        
        with tab3:
            st.subheader("Price vs Purchase Frequency Correlation")
            query = """SELECT products.product_category, 
                             COUNT(order_items.product_id) as purchase_count,
                             ROUND(AVG(order_items.price), 2) as avg_price
                      FROM products JOIN order_items ON products.product_id = order_items.product_id
                      GROUP BY products.product_category
                      HAVING purchase_count > 100
                      ORDER BY purchase_count DESC"""
            
            result = execute_query(query, db_connection)
            
            if result:
                df = pd.DataFrame(result, columns=["Category", "Purchase Count", "Average Price"])
                
                correlation = np.corrcoef(df["Purchase Count"], df["Average Price"])[0, 1]
                st.metric("Correlation Coefficient", f"{correlation:.4f}")
                
                fig = px.scatter(df, x="Average Price", y="Purchase Count", 
                               hover_data=["Category"],
                               title=f"Price vs Purchase Frequency (Correlation: {correlation:.4f})")
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(df)
    
    # Time Series Analysis
    elif analysis_type == "📈 Time Series Analysis":
        st.header("Time Series Analysis")
        
        tab1, tab2, tab3 = st.tabs(["Cumulative Sales", "Year-over-Year Growth", "Moving Average"])
        
        with tab1:
            st.subheader("Cumulative Sales by Month")
            query = """SELECT years, months, payment, 
                             SUM(payment) OVER(ORDER BY years, months) as cumulative_sales 
                      FROM 
                      (SELECT YEAR(orders.order_purchase_timestamp) as years,
                              MONTH(orders.order_purchase_timestamp) as months,
                              ROUND(SUM(payments.payment_value), 2) as payment 
                       FROM orders JOIN payments ON orders.order_id = payments.order_id
                       GROUP BY years, months 
                       ORDER BY years, months) as a"""
            
            result = execute_query(query, db_connection)
            
            if result:
                df = pd.DataFrame(result, columns=["Year", "Month", "Monthly Sales", "Cumulative Sales"])
                df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
                
                fig = px.line(df, x="Date", y="Cumulative Sales",
                            title="Cumulative Sales Over Time")
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(df)
        
        with tab2:
            st.subheader("Year-over-Year Growth Rate")
            query = """WITH yearly_sales AS (
                        SELECT YEAR(orders.order_purchase_timestamp) as years,
                               ROUND(SUM(payments.payment_value), 2) as payment 
                        FROM orders JOIN payments ON orders.order_id = payments.order_id
                        GROUP BY years 
                        ORDER BY years
                      )
                      SELECT years, payment,
                             ROUND(((payment - LAG(payment, 1) OVER(ORDER BY years))/
                                   LAG(payment, 1) OVER(ORDER BY years)) * 100, 2) as yoy_growth
                      FROM yearly_sales"""
            
            result = execute_query(query, db_connection)
            
            if result:
                df = pd.DataFrame(result, columns=["Year", "Sales", "YoY Growth %"])
                
                fig = px.bar(df[df["YoY Growth %"].notna()], x="Year", y="YoY Growth %",
                           title="Year-over-Year Growth Rate")
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(df)
        
        with tab3:
            st.subheader("Moving Average of Order Values")
            query = """SELECT customer_id, order_purchase_timestamp, payment,
                             AVG(payment) OVER(PARTITION BY customer_id 
                                              ORDER BY order_purchase_timestamp
                                              ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg
                      FROM
                      (SELECT orders.customer_id, orders.order_purchase_timestamp, 
                              payments.payment_value as payment
                       FROM payments JOIN orders ON payments.order_id = orders.order_id) as a
                      ORDER BY customer_id, order_purchase_timestamp
                      LIMIT 1000"""
            
            result = execute_query(query, db_connection)
            
            if result:
                df = pd.DataFrame(result, columns=["Customer ID", "Date", "Payment", "Moving Average"])
                
                # Show sample for first few customers
                sample_customers = df["Customer ID"].unique()[:5]
                sample_df = df[df["Customer ID"].isin(sample_customers)]
                
                fig = px.line(sample_df, x="Date", y="Moving Average", 
                            color="Customer ID",
                            title="Moving Average of Order Values (Sample Customers)")
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(df.head(100))
    
    # Customer Retention
    elif analysis_type == "🔄 Customer Retention":
        st.header("Customer Retention Analysis")
        
        st.subheader("6-Month Retention Rate")
        query = """WITH first_orders AS (
                    SELECT customers.customer_id,
                           MIN(orders.order_purchase_timestamp) as first_order
                    FROM customers JOIN orders ON customers.customer_id = orders.customer_id
                    GROUP BY customers.customer_id
                  ),
                  repeat_customers AS (
                    SELECT a.customer_id, 
                           COUNT(DISTINCT orders.order_purchase_timestamp) as repeat_orders
                    FROM first_orders a JOIN orders ON orders.customer_id = a.customer_id
                    AND orders.order_purchase_timestamp > first_order
                    AND orders.order_purchase_timestamp < DATE_ADD(first_order, INTERVAL 6 MONTH)
                    GROUP BY a.customer_id
                  ) 
                  SELECT 
                    COUNT(DISTINCT first_orders.customer_id) as total_customers,
                    COUNT(DISTINCT repeat_customers.customer_id) as retained_customers,
                    ROUND(100 * COUNT(DISTINCT repeat_customers.customer_id) / 
                          COUNT(DISTINCT first_orders.customer_id), 2) as retention_rate
                  FROM first_orders 
                  LEFT JOIN repeat_customers ON first_orders.customer_id = repeat_customers.customer_id"""
        
        result = execute_query(query, db_connection)
        
        if result:
            total_customers, retained_customers, retention_rate = result[0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Customers", f"{total_customers:,}")
            
            with col2:
                st.metric("Retained Customers", f"{retained_customers:,}")
            
            with col3:
                st.metric("Retention Rate", f"{retention_rate}%")
            
            # Visualization
            fig = go.Figure(data=[
                go.Bar(name='Lost Customers', x=['6-Month Period'], 
                      y=[total_customers - retained_customers]),
                go.Bar(name='Retained Customers', x=['6-Month Period'], 
                      y=[retained_customers])
            ])
            fig.update_layout(barmode='stack', title='Customer Retention Breakdown')
            st.plotly_chart(fig, use_container_width=True)
    
    # Top Performers
    elif analysis_type == "🏆 Top Performers":
        st.header("Top Performers")
        
        tab1, tab2 = st.tabs(["Top Sellers", "Top Customers by Year"])
        
        with tab1:
            st.subheader("Top Revenue-Generating Sellers")
            query = """SELECT seller_id, ROUND(revenue, 2) as revenue, 
                             DENSE_RANK() OVER(ORDER BY revenue DESC) as ranking
                      FROM
                      (SELECT order_items.seller_id, SUM(payments.payment_value) as revenue
                       FROM order_items JOIN payments ON order_items.order_id = payments.order_id
                       GROUP BY order_items.seller_id) as a
                      ORDER BY revenue DESC
                      LIMIT 15"""
            
            result = execute_query(query, db_connection)
            
            if result:
                df = pd.DataFrame(result, columns=["Seller ID", "Revenue", "Rank"])
                
                fig = px.bar(df, x="Seller ID", y="Revenue",
                           title="Top 15 Sellers by Revenue")
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(df)
        
        with tab2:
            st.subheader("Top 3 Customers by Spending (Each Year)")
            query = """SELECT years, customer_id, ROUND(payment, 2) as payment, ranking
                      FROM
                      (SELECT YEAR(orders.order_purchase_timestamp) as years,
                              orders.customer_id,
                              SUM(payments.payment_value) as payment,
                              DENSE_RANK() OVER(PARTITION BY YEAR(orders.order_purchase_timestamp)
                                               ORDER BY SUM(payments.payment_value) DESC) as ranking
                       FROM orders JOIN payments ON payments.order_id = orders.order_id
                       GROUP BY YEAR(orders.order_purchase_timestamp), orders.customer_id) as a
                      WHERE ranking <= 3
                      ORDER BY years, ranking"""
            
            result = execute_query(query, db_connection)
            
            if result:
                df = pd.DataFrame(result, columns=["Year", "Customer ID", "Payment", "Rank"])
                
                fig = px.bar(df, x="Customer ID", y="Payment", color="Year",
                           title="Top 3 Customers by Year")
                fig.update_xaxes(tickangle=45)
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
