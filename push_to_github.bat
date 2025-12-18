@echo off
chcp 65001 > nul
echo.
echo ========================================
echo   NutriSnap AI - GitHub 推送脚本
echo ========================================
echo.

REM 检查是否已初始化 Git
if not exist ".git" (
    echo 📦 初始化 Git 仓库...
    git init
    if errorlevel 1 (
        echo ❌ Git 初始化失败！请确保已安装 Git。
        echo 下载地址：https://git-scm.com/download/win
        pause
        exit /b 1
    )
    echo ✅ Git 仓库初始化成功
    echo.
)

echo 📋 添加文件到 Git...
git add app.py requirements.txt README.md .gitignore
if errorlevel 1 (
    echo ❌ 添加文件失败！
    pause
    exit /b 1
)
echo ✅ 文件添加成功
echo.

echo 📝 创建提交...
git commit -m "Initial commit: NutriSnap AI demo application"
if errorlevel 1 (
    echo ⚠️ 提交失败或没有变更
)
echo.

echo ========================================
echo   下一步操作说明：
echo ========================================
echo.
echo 1. 前往 https://github.com 登录您的账号
echo 2. 点击右上角 "+" 号，选择 "New repository"
echo 3. 仓库名称输入：nutrisnap-ai（或其他名称）
echo 4. 选择 "Public"（公开）
echo 5. 不要勾选 "Initialize with README"  
echo 6. 点击 "Create repository"
echo.
echo 7. 复制仓库地址，格式如：
echo    https://github.com/your-username/nutrisnap-ai.git
echo.
echo 8. 运行以下命令（替换成您的仓库地址）：
echo.
echo    git remote add origin https://github.com/your-username/nutrisnap-ai.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 9. 完成后访问 https://streamlit.io/cloud 部署应用
echo.
echo ========================================
pause
