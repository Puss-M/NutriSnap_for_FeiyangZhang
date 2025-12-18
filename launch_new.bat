@echo off
echo ======================================
echo   Starting NutriSnap with New Features
echo ======================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install streamlit requests >nul 2>&1

REM Run the app
echo.
echo Starting Streamlit app...
echo Open your browser to http://localhost:8501
echo.
streamlit run app.py

pause
