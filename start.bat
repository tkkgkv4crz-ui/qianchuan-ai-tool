@echo off
chcp 65001 >nul
cls
echo.
echo   ╔══════════════════════════════════════════════════════════╗
echo   ║  千川AI投放工具 - 本地一键启动 v1.0                        ║
echo   ║  基于FastAPI + Vue3 的巨量千川开放平台智能投放管理系统         ║
echo   ╚══════════════════════════════════════════════════════════╝
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.10+ 并添加到环境变量
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

set BACKEND_DIR=%~dp0backend
set VENV_DIR=%BACKEND_DIR%\venv

if not exist "%BACKEND_DIR%\app\main.py" (
    echo [错误] 找不到后端目录: %BACKEND_DIR%
    pause
    exit /b 1
)

echo [信息] 后端目录: %BACKEND_DIR%

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [信息] 创建虚拟环境...
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo [完成] 虚拟环境创建完成
) else (
    echo [完成] 虚拟环境已存在
)

echo [信息] 安装依赖包（首次运行可能需要几分钟）...
"%VENV_DIR%\Scripts\pip.exe" install -q --upgrade pip
"%VENV_DIR%\Scripts\pip.exe" install -q -r "%BACKEND_DIR%\requirements.txt"
if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败，请检查网络连接
    pause
    exit /b 1
)
echo [完成] 依赖安装完成

if not exist "%BACKEND_DIR%\.env" (
    echo [信息] 创建 .env 配置文件...
    copy "%BACKEND_DIR%\.env.example" "%BACKEND_DIR%\.env" >nul
    echo [完成] .env 已创建（请编辑填写你的 AppID 和 AppSecret）
) else (
    echo [完成] .env 配置文件已存在
)

if not exist "%BACKEND_DIR%\logs" mkdir "%BACKEND_DIR%\logs"

echo.
echo ═════════════════════════════════════════════════════════════
echo 正在启动千川AI投放工具服务...
echo ═════════════════════════════════════════════════════════════
echo.
echo 前端页面: http://localhost:8000
echo API文档:  http://localhost:8000/docs
echo.

start /b cmd /c "timeout /t 5 >nul & start http://localhost:8000"

cd /d "%BACKEND_DIR%"
set PYTHONPATH=%BACKEND_DIR%
"%VENV_DIR%\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo [信息] 服务已停止
echo 按任意键关闭窗口...
pause >nul
