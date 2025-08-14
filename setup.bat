@echo off
echo ====================================
echo E-Commerce Dashboard Setup Script
echo ====================================
echo.

echo Step 1: Installing required packages...
echo ----------------------------------------
pip install -r requirements.txt

echo.
echo Step 2: Testing database connection...
echo ----------------------------------------
python test_connection.py

echo.
echo ====================================
echo Setup Instructions:
echo ====================================
echo.
echo 1. FIRST: Make sure you've run your Jupyter notebook
echo    to load CSV data into MySQL database
echo.
echo 2. THEN: Run the dashboard with:
echo    streamlit run streamlit_app.py
echo.
echo 3. OPEN: http://localhost:8501 in your browser
echo.
echo 4. SHARE: Use your IP + port 8501 to share with others
echo    Find your IP with: ipconfig
echo.
echo ====================================
pause
