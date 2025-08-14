@echo off
echo 🚀 Starting E-Commerce Dashboard...
echo ====================================
echo.

echo Checking if everything is ready...
python test_connection.py

echo.
echo Starting Streamlit dashboard...
echo Opening http://localhost:8501 in your browser...
echo.
echo 💡 To stop the dashboard: Press Ctrl+C
echo.

streamlit run streamlit_app.py
