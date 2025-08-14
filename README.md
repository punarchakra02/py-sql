# E-Commerce Data Analysis Dashboard

A comprehensive Streamlit dashboard for analyzing e-commerce data stored in MySQL database. This dashboard provides insights into customer behavior, sales trends, and business performance metrics.

## ⚠️ **IMPORTANT: Read This First**

This Streamlit app **READS** data from your MySQL database. It does **NOT** load CSV files. 

**You must run your notebook first to load data into MySQL, then run the Streamlit app.**

## 🔄 **Complete Setup Process**

### **Step 1: Load Data into Database (Run Notebook First)**

1. **Open your Jupyter notebook**: `python+sql ecommerce.ipynb`
2. **Run the first cell** to load CSV data into MySQL database
3. **Verify data is loaded** by running a few query cells
4. **Only then proceed to Step 2**

### **Step 2: Run Streamlit Dashboard**

## Features

- 📊 **Overview Dashboard**: Key metrics and summary statistics
- 🏙️ **Customer Analysis**: Geographic distribution and customer insights
- 📦 **Order Analysis**: Order patterns and trends over time
- 💰 **Sales & Revenue**: Category-wise performance and revenue analysis
- 📈 **Time Series Analysis**: Growth trends and moving averages
- 🔄 **Customer Retention**: Retention rates and customer lifecycle
- 🏆 **Top Performers**: Best sellers and top customers

## Prerequisites

- ✅ Python 3.7 or higher
- ✅ MySQL server running on localhost
- ✅ CSV files already loaded into MySQL database (via notebook)
- ✅ Database named 'ECOM' with tables: customers, orders, products, payments, order_items, sellers

## Installation & Setup

### **Option A: Quick Setup (Recommended)**

1. **Navigate to project folder**:
   ```cmd
   cd "c:\Users\gloon\Downloads\punar"
   ```

2. **Run setup script**:
   ```cmd
   setup.bat
   ```

3. **Test database connection**:
   ```cmd
   python test_connection.py
   ```

4. **Start dashboard**:
   ```cmd
   streamlit run streamlit_app.py
   ```

### **Option B: Manual Setup**

1. **Install packages**:
   ```cmd
   pip install -r requirements.txt
   ```

2. **Verify database connection** (see test script below)

3. **Start dashboard**:
   ```cmd
   streamlit run streamlit_app.py
   ```

## 🧪 **Testing Your Setup**

Before running Streamlit, test if everything is ready:

```cmd
python test_connection.py
```

This will check:
- ✅ Database connection
- ✅ Required tables exist  
- ✅ Data is present
- ✅ Sample queries work

## Running the Application

### **Method 1: Local Only**
```cmd
streamlit run streamlit_app.py
```
**Access at**: `http://localhost:8501`

### **Method 2: Share on Network**
```cmd
streamlit run streamlit_app.py --server.address 0.0.0.0
```
**Share with others**: `http://YOUR_IP:8501`

## 🌐 Deployment & Sharing Options

### **1. Streamlit Cloud (Free & Easy)**

**Perfect for sharing your project publicly:**

1. **Push to GitHub**:
   ```cmd
   git init
   git add .
   git commit -m "E-commerce dashboard"
   git push origin main
   ```

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

### **3. Heroku/Railway/Render**

Professional hosting with custom domains available.

## 🔧 Database Schema

The dashboard expects these tables in your MySQL 'ECOM' database:

| Table | Purpose |
|-------|---------|
| `customers` | Customer information and location |
| `orders` | Order details and timestamps |
| `order_items` | Individual items in each order |
| `products` | Product catalog and categories |
| `payments` | Payment information and values |
| `sellers` | Seller information |
| `geolocation` | Geographic coordinates |

## 🐛 Troubleshooting

### **"Database connection failed"**
- ✅ Check MySQL server is running
- ✅ Verify credentials in `streamlit_app.py`
- ✅ Confirm database 'ECOM' exists
- ✅ Run `python test_connection.py`

### **"Table doesn't exist"**
- ✅ Run your notebook first to load CSV data
- ✅ Check table names match exactly
- ✅ Verify data loaded with test script

### **"No module named 'streamlit'"**
- ✅ Install packages: `pip install -r requirements.txt`
- ✅ Use virtual environment if needed
- ✅ Check Python version (3.7+)

### **Charts not showing**
- ✅ Check browser console for errors
- ✅ Try refreshing the page
- ✅ Verify data exists in database

### **Performance issues**
- ✅ Add database indexes for large datasets
- ✅ Limit query results for testing
- ✅ Use caching (already implemented)

## 🚀 **Quick Start Checklist**

- [ ] MySQL server running
- [ ] Notebook executed (CSV data loaded)
- [ ] Packages installed (`pip install -r requirements.txt`)
- [ ] Connection tested (`python test_connection.py`)
- [ ] Dashboard started (`streamlit run streamlit_app.py`)
- [ ] Browser opened (`http://localhost:8501`)

## 💡 **Pro Tips**

1. **Portfolio Ready**: This dashboard showcases SQL, Python, and data visualization skills
2. **Customizable**: Easy to modify queries and add new analyses  
3. **Shareable**: Multiple deployment options for different audiences
4. **Interactive**: Much more engaging than static notebook outputs

## 📞 **Getting Help**

1. **Test first**: Always run `python test_connection.py`
2. **Check logs**: Streamlit shows helpful error messages
3. **Verify data**: Ensure your notebook ran successfully
4. **Network issues**: Try `localhost:8501` vs `127.0.0.1:8501`

## 🎯 **What Makes This Special**

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

### 2. Local Network Sharing

To share with others on your local network:

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

Then share your IP address with port 8501 (e.g., `http://192.168.1.100:8501`)

### 3. Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY streamlit_app.py .
EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t ecommerce-dashboard .
docker run -p 8501:8501 ecommerce-dashboard
```

## Security Notes

⚠️ **Important**: 
- Never commit database passwords to version control
- Use environment variables or Streamlit secrets for sensitive data
- Consider using connection pooling for production deployments

## Customization

You can customize the dashboard by:
- Modifying queries in `streamlit_app.py`
- Adding new analysis sections
- Changing visualization styles
- Adding filters and interactive elements

## Troubleshooting

**Database Connection Issues**:
- Verify MySQL server is running
- Check database credentials
- Ensure database and tables exist

**Package Installation Issues**:
- Use a virtual environment
- Upgrade pip: `pip install --upgrade pip`
- Install packages individually if bulk install fails

**Performance Issues**:
- Add database indexing for frequently queried columns
- Implement caching for expensive queries
- Consider data pagination for large datasets

## Support

For issues or questions:
1. Check the error messages in the Streamlit interface
2. Verify database connectivity
3. Ensure all required packages are installed

## License

This project is for educational and demonstration purposes.
