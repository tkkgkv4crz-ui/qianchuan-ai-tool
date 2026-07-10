#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
千川AI投放工具 - 本地一键启动器
===============================
双击运行即可自动完成环境检查、依赖安装、启动服务并打开浏览器。

用法:
    python launcher.py              # 启动服务
    python launcher.py --install    # 仅安装依赖（不启动服务）
    python launcher.py --build      # 打包成 exe（需要安装 PyInstaller）
"""

import sys
import os
import subprocess
import time
import threading
import webbrowser
from pathlib import Path
import shutil

# 颜色输出（Windows兼容）
try:
    from colorama import init, Fore, Style
    init()
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    RESET = Style.RESET_ALL
except ImportError:
    RED = GREEN = YELLOW = BLUE = CYAN = RESET = ""

def banner():
    print(f"""
{CYAN}╔══════════════════════════════════════════════════════════╗
║  千川AI投放工具 - 本地一键启动器 v1.0                      ║
║  基于FastAPI + Vue3 的巨量千川开放平台智能投放管理系统         ║
╚══════════════════════════════════════════════════════════╝{RESET}
""")

def log(msg, level="INFO"):
    """打印带颜色的日志"""
    colors = {"INFO": BLUE, "OK": GREEN, "WARN": YELLOW, "ERR": RED}
    c = colors.get(level, RESET)
    print(f"{c}[{level}]{RESET} {msg}")

def check_python():
    """检查 Python 版本"""
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 10):
        log(f"Python 版本 {v.major}.{v.minor} 过低，需要 Python 3.10+", "ERR")
        log("请访问 https://www.python.org/downloads/ 下载安装 Python 3.10+", "ERR")
        return False
    log(f"Python 版本: {v.major}.{v.minor}.{v.micro} ✅", "OK")
    return True

def find_backend_dir():
    """查找后端目录"""
    candidates = [
        Path(__file__).parent / "backend",
        Path(__file__).parent / "qianchuan-ai-tool" / "backend",
        Path.cwd() / "backend",
        Path.cwd() / "qianchuan-ai-tool" / "backend",
    ]
    for p in candidates:
        if (p / "app" / "main.py").exists():
            return p.resolve()
    return None

def setup_venv(backend_dir):
    """创建虚拟环境"""
    venv_dir = backend_dir / "venv"
    if venv_dir.exists():
        log("虚拟环境已存在，跳过创建", "OK")
        return venv_dir
    log("创建虚拟环境...", "INFO")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        log(f"虚拟环境创建完成: {venv_dir}", "OK")
        return venv_dir
    except Exception as e:
        log(f"创建虚拟环境失败: {e}", "ERR")
        return None

def get_pip(venv_dir):
    """获取虚拟环境中的 pip 路径"""
    if os.name == "nt":
        pip = venv_dir / "Scripts" / "pip.exe"
        python = venv_dir / "Scripts" / "python.exe"
    else:
        pip = venv_dir / "bin" / "pip"
        python = venv_dir / "bin" / "python"
    return str(pip), str(python)

def install_deps(venv_dir, backend_dir):
    """安装依赖"""
    pip, _ = get_pip(venv_dir)
    req_file = backend_dir / "requirements.txt"
    if not req_file.exists():
        log(f"找不到依赖文件: {req_file}", "ERR")
        return False
    log("安装依赖包（可能需要几分钟，请等待）...", "INFO")
    try:
        subprocess.run([pip, "install", "--upgrade", "pip"], capture_output=True)
        result = subprocess.run(
            [pip, "install", "-r", str(req_file)],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            log("依赖安装完成 ✅", "OK")
            return True
        else:
            log(f"依赖安装失败:\n{result.stderr}", "ERR")
            return False
    except subprocess.TimeoutExpired:
        log("安装超时，请检查网络连接", "ERR")
        return False
    except Exception as e:
        log(f"安装依赖出错: {e}", "ERR")
        return False

def create_env_file(backend_dir):
    """创建 .env 配置文件"""
    env_file = backend_dir / ".env"
    env_example = backend_dir / ".env.example"
    if env_file.exists():
        log(".env 配置文件已存在", "OK")
        return True
    if not env_example.exists():
        log("找不到 .env.example 模板", "WARN")
        return False
    with open(env_example, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(
        "QC_REDIRECT_URI=http://localhost:8000/auth/callback",
        "QC_REDIRECT_URI=http://localhost:8000/api/v1/auth/callback"
    )
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(content)
    log(f".env 配置文件已创建: {env_file}", "OK")
    log("⚠️ 请编辑 .env 文件，填写你的 AppID 和 AppSecret", "WARN")
    return True

def start_server(venv_dir, backend_dir):
    """启动后端服务"""
    _, python = get_pip(venv_dir)
    log("正在启动后端服务...", "INFO")
    logs_dir = backend_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(backend_dir)
    cmd = [python, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    log(f"启动命令: {' '.join(cmd)}", "INFO")
    log("服务启动中，请等待 3-5 秒...", "INFO")
    try:
        proc = subprocess.Popen(
            cmd, cwd=str(backend_dir), env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", bufsize=1
        )
        return proc
    except Exception as e:
        log(f"启动服务失败: {e}", "ERR")
        return None

def tail_logs(proc):
    """实时输出服务日志"""
    for line in proc.stdout:
        line = line.strip()
        if line:
            print(f"  [后端] {line}")

def open_browser(delay=3):
    """延迟打开浏览器"""
    time.sleep(delay)
    url = "http://localhost:8000"
    log(f"正在打开浏览器: {url}", "INFO")
    try:
        webbrowser.open(url)
    except Exception as e:
        log(f"自动打开浏览器失败，请手动访问: {url}", "WARN")

def build_exe():
    """使用 PyInstaller 打包成 exe"""
    log("开始打包成 exe...", "INFO")
    try:
        import PyInstaller
        log("PyInstaller 已安装", "OK")
    except ImportError:
        log("PyInstaller 未安装，尝试安装...", "WARN")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            log("PyInstaller 安装完成", "OK")
        except Exception as e:
            log(f"PyInstaller 安装失败: {e}", "ERR")
            return False
    backend_dir = find_backend_dir()
    if not backend_dir:
        log("找不到后端目录，无法打包", "ERR")
        return False
    root = backend_dir.parent
    log("请手动运行以下命令完成打包:", "INFO")
    log(f"  cd {root}", "INFO")
    log(f"  pyinstaller launcher.py --onefile --name 千川AI投放工具", "INFO")
    log("\n打包完成后，dist/目录下会生成 exe", "INFO")
    return True

def main():
    banner()
    if "--build" in sys.argv:
        build_exe()
        return
    install_only = "--install" in sys.argv
    if not check_python():
        input("\n按回车键退出...")
        sys.exit(1)
    backend_dir = find_backend_dir()
    if not backend_dir:
        log("找不到后端目录", "ERR")
        input("\n按回车键退出...")
        sys.exit(1)
    log(f"后端目录: {backend_dir}", "OK")
    venv_dir = setup_venv(backend_dir)
    if not venv_dir:
        input("\n按回车键退出...")
        sys.exit(1)
    if not install_deps(venv_dir, backend_dir):
        input("\n按回车键退出...")
        sys.exit(1)
    create_env_file(backend_dir)
    if install_only:
        log("依赖安装完成，已退出", "OK")
        return
    log("\n" + "=" * 50, "INFO")
    log("正在启动千川AI投放工具服务...", "INFO")
    log("=" * 50, "INFO")
    proc = start_server(venv_dir, backend_dir)
    if not proc:
        input("\n按回车键退出...")
        sys.exit(1)
    log_thread = threading.Thread(target=tail_logs, args=(proc,), daemon=True)
    log_thread.start()
    browser_thread = threading.Thread(target=open_browser, args=(4,), daemon=True)
    browser_thread.start()
    log("\n服务已启动！", "OK")
    log("前端页面: http://localhost:8000", "OK")
    log("API文档: http://localhost:8000/docs", "OK")
    log("\n⚠️ 首次使用请先在千川开放平台创建应用并获取 AppID/AppSecret", "WARN")
    log("然后编辑 backend/.env 文件填入配置，重启服务即可授权使用", "WARN")
    log("\n按 Ctrl+C 停止服务", "INFO")
    try:
        proc.wait()
    except KeyboardInterrupt:
        log("\n收到停止信号，正在关闭服务...", "INFO")
        proc.terminate()
        proc.wait(timeout=5)
        log("服务已停止", "OK")

if __name__ == "__main__":
    main()
