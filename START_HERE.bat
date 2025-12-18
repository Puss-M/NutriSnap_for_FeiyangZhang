@echo off
echo ======================================
echo   NutriSnap AI - 完整版启动脚本
echo ======================================
echo.

echo [1/3] 删除旧的虚拟环境...
if exist venv_fresh rmdir /s /q venv_fresh

echo [2/3] 创建新的虚拟环境...
python -m venv venv_fresh
if errorlevel 1 (
    echo ❌ 虚拟环境创建失败！
    echo 请确保已安装 Python 3.7+
    pause
    exit /b 1
)

echo [3/3] 安装依赖并启动应用...
call venv_fresh\Scripts\activate.bat
python -m pip install --upgrade pip >nul
python -m pip install streamlit requests

echo.
echo ✅ 准备就绪！正在启动 NutriSnap AI...
echo 📱 浏览器将打开 http://localhost:8501
echo.

streamlit run app.py

pause
