"""
Database Connection Test Script
Run this before starting the Streamlit dashboard
"""

import mysql.connector
import sys

def test_database_connection():
    """Test database connection and verify data exists"""
    
    print("🔍 Testing Database Connection...")
    print("=" * 50)
    
    try:
        # Test connection
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Punarbasu_03',  # Update if different
            database='ECOM'
        )
        cursor = conn.cursor()
        print("✅ Database connection successful!")
        
        # Test required tables
        required_tables = ['customers', 'orders', 'products', 'payments', 'order_items', 'sellers']
        
        print("\n📋 Checking required tables...")
        cursor.execute("SHOW TABLES")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        missing_tables = []
        for table in required_tables:
            if table in existing_tables:
                print(f"✅ Table '{table}' exists")
            else:
                print(f"❌ Table '{table}' MISSING")
                missing_tables.append(table)
        
        if missing_tables:
            print(f"\n⚠️  Missing tables: {', '.join(missing_tables)}")
            print("💡 Run your notebook first to load CSV data into database!")
            return False
        
        # Test data exists
        print("\n📊 Checking data in tables...")
        data_checks = [
            ("customers", "SELECT COUNT(*) FROM customers"),
            ("orders", "SELECT COUNT(*) FROM orders"),
            ("products", "SELECT COUNT(*) FROM products"),
            ("payments", "SELECT COUNT(*) FROM payments")
        ]
        
        all_data_exists = True
        for table_name, query in data_checks:
            cursor.execute(query)
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"✅ {table_name}: {count:,} records")
            else:
                print(f"❌ {table_name}: No data found")
                all_data_exists = False
        
        if not all_data_exists:
            print("\n⚠️  Some tables are empty!")
            print("💡 Run your notebook to load CSV data first!")
            return False
        
        # Test a sample query
        print("\n🧪 Testing sample query...")
        cursor.execute("SELECT COUNT(DISTINCT customer_city) FROM customers")
        city_count = cursor.fetchone()[0]
        print(f"✅ Found {city_count} unique customer cities")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 All tests passed! Ready to run Streamlit dashboard!")
        print("\nNext step: streamlit run streamlit_app.py")
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ Database connection failed: {err}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Is MySQL server running?")
        print("   2. Are credentials correct?")
        print("   3. Does database 'ECOM' exist?")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_streamlit_packages():
    """Test if required packages are installed"""
    
    print("\n🐍 Testing Python packages...")
    print("=" * 50)
    
    required_packages = [
        'streamlit',
        'pandas', 
        'matplotlib',
        'seaborn',
        'mysql.connector',
        'numpy',
        'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'mysql.connector':
                import mysql.connector
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("💡 Install with: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages installed!")
        return True

if __name__ == "__main__":
    print("🚀 E-Commerce Dashboard Setup Test")
    print("=" * 50)
    
    # Test packages first
    packages_ok = test_streamlit_packages()
    
    # Test database connection
    database_ok = test_database_connection()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY:")
    
    if packages_ok and database_ok:
        print("🎉 Everything looks good!")
        print("✅ Ready to run: streamlit run streamlit_app.py")
    else:
        print("❌ Issues found. Please fix the problems above.")
        if not packages_ok:
            print("   - Install missing packages")
        if not database_ok:
            print("   - Fix database connection/data issues")
    
    print("\n💡 Need help? Check the README.md file")
    
    # Keep window open on Windows
    input("\nPress Enter to exit...")
