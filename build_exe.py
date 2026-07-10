#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
千川AI投放工具 - EXE 打包脚本
运行此脚本自动将 launcher.py 打包成 Windows 可执行文件 (.exe)
用法: python build_exe.py
"""

import sys
import subprocess
from pathlib import Path


def check_pyinstaller():
    try:
        import PyInstaller
        print("[✅] PyInstaller 已安装")
        return True
    except ImportError:
        print("[❌] PyInstaller 未安装")
        return False


def install_pyinstaller():
    print("[📦] 正在安装 PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "colorama"], check=True)
        print("[✅] 安装完成")
        return True
    except Exception as e:
        print(f"[❌] 安装失败: {e}")
        return False


def build_exe():
    root = Path(__file__).parent.resolve()
    launcher = root / "launcher.py"
    if not launcher.exists():
        print(f"[❌] 找不到 launcher.py")
        return False

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile", "--name", "千川AI投放工具",
        "--distpath", str(root / "dist"),
        "--workpath", str(root / "build"),
        "--specpath", str(root),
        "--add-data", f"{root / 'backend'};backend",
        "--add-data", f"{root / 'frontend'};frontend",
        "--hidden-import", "fastapi", "--hidden-import", "uvicorn",
        "--hidden-import", "pydantic", "--hidden-import", "httpx",
        "--hidden-import", "jose", "--hidden-import", "sqlalchemy",
        "--hidden-import", "aiosqlite", "--hidden-import", "apscheduler",
        "--hidden-import", "dotenv", "--hidden-import", "pandas",
        "--hidden-import", "numpy", "--hidden-import", "colorama",
        str(launcher)
    ]

    print("[📦] 开始打包...")
    try:
        subprocess.run(cmd, check=True)
        print(f"[✅] 打包完成: {root / 'dist' / '千川AI投放工具.exe'}")
        return True
    except Exception as e:
        print(f"[❌] 打包失败: {e}")
        return False


def main():
    if not check_pyinstaller():
        if not install_pyinstaller():
            sys.exit(1)
    build_exe()


if __name__ == "__main__":
    main()
