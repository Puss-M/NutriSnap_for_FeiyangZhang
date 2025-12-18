@echo off
echo ======================================
echo   NutriSnap AI - 快速启动
echo ======================================
echo.
echo 正在启动应用...
echo 浏览器将自动打开 http://localhost:8501
echo.
echo 提示: 如遇到错误，请升级 Python 到 3.10+ 正式版
echo.

python -m pip install --upgrade "streamlit<1.30" requests --quiet
python -m streamlit run app.py

pause
