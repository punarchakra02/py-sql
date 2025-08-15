# E-Commerce Data Analysis Dashboard

A comprehensive Streamlit dashboard for analyzing e-commerce data stored in MySQL database. This dashboard provides insights into customer behavior, sales trends, and business performance metrics.



## Features

-  **Overview Dashboard**: Key metrics and summary statistics
-  **Customer Analysis**: Geographic distribution and customer insights
-  **Order Analysis**: Order patterns and trends over time
-  **Sales & Revenue**: Category-wise performance and revenue analysis
-  **Time Series Analysis**: Growth trends and moving averages
-  **Customer Retention**: Retention rates and customer lifecycle
-  **Top Performers**: Best sellers and top customers

## Prerequisites

- ✅ Python 3.7 or higher
- ✅SQLite server running on streamlit
- ✅ CSV files already loaded into SQLite database (via notebook)
- ✅ Database named 'ECOM' with tables: customers, orders, products, payments, order_items, sellers



### **Method 2: Share on Network**
```cmd
streamlit run streamlit_app.py --server.address 0.0.0.0
```
**Share with others**: `http://YOUR_IP:8501`


2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `streamlit_app.py`
   
3. **Add database secrets** (in Streamlit Cloud dashboard):
   ```toml
   [mysql]
   host = "your-cloud-database-host"
   user = "your-username"  
   password = "your-password"
   database = "ECOM"
   ```

**Note**: You'll need a cloud MySQL database (like PlanetScale, Railway, or AWS RDS) for Streamlit Cloud.

### **2. Local Network Sharing**

**Share with colleagues on same network:**

```cmd
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```

Find your IP and share: `http://YOUR_IP:8501`

##  **What Makes This Special**

This isn't just a dashboard - it's a **professional data analysis portfolio piece** that demonstrates:

- **SQL expertise**: Complex queries with JOINs, CTEs, window functions
- **Python skills**: Data processing, visualization, web app development  
- **Business insight**: Meaningful metrics like retention, growth, top performers
- **Technical deployment**: Multiple hosting and sharing options

Perfect for job interviews, client presentations, or portfolio showcases!

## Database Schema

The application expects the following tables in your MySQL database:
- `customers`: Customer information
- `orders`: Order details and timestamps
- `order_items`: Individual items in orders
- `products`: Product catalog
- `payments`: Payment information
- `sellers`: Seller information
- `geolocation`: Geographic data

## Deployment Options

### 1. Streamlit Cloud (Recommended)

1. **Push code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select the `streamlit_app.py` file
   - Configure secrets for database credentials

3. **Add secrets in Streamlit Cloud**:
   ```toml
   [mysql]
   host = "your-host"
   user = "your-username"
   password = "your-password"
   database = "ECOM"
   ```

## License

This project is for educational and demonstration purposes.
