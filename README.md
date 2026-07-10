# 千川AI投放工具 - 本地部署指南

## 快速开始（3分钟上手）

### 方式一：双击启动（推荐）

**Windows 用户：**
```
双击 start.bat  → 自动检查环境 → 安装依赖 → 启动服务 → 自动打开浏览器
```

**Mac/Linux 用户：**
```bash
./start.sh
```

### 方式二：Python 启动器

```bash
python launcher.py
```

参数说明：
- `python launcher.py` — 正常启动
- `python launcher.py --install` — 仅安装依赖
- `python launcher.py --build` — 生成 PyInstaller 打包配置

---

## 手动部署

### 1. 环境要求
- Python 3.10+
- 网络连接（首次安装依赖需要）

### 2. 安装依赖

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\pip install -r requirements.txt

# Mac/Linux
venv/bin/pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
vim .env
```

必须修改的配置项：
```
QC_APP_ID=你的AppID
QC_APP_SECRET=你的AppSecret
```

### 4. 启动服务

```bash
cd backend
set PYTHONPATH=%CD%
venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. 打开浏览器

访问 http://localhost:8000

---

## 千川开放平台授权配置

### 1. 注册开放平台账号
访问 https://open.oceanengine.com/ 注册并创建应用

### 2. 创建应用并获取凭证
- 创建应用 → 获取 `AppID` 和 `AppSecret`
- 申请权限：千川PC全域投放、广告投放管理、数据报表、素材管理、随心推投放管理

### 3. 配置回调地址
```
http://localhost:8000/api/v1/auth/callback
```

### 4. 填入 .env 文件
```bash
QC_APP_ID=your_app_id
QC_APP_SECRET=your_app_secret
QC_REDIRECT_URI=http://localhost:8000/api/v1/auth/callback
```

### 5. 重启服务并授权

---

## 打包成 EXE（可选）

```bash
python build_exe.py
```

打包完成后，在 `dist/` 目录下会生成 `.exe` 文件。

> 注意：打包后的 exe 体积较大（约 50-100MB），因为需要包含整个 Python 运行时。建议直接使用 `start.bat` 或 `launcher.py` 启动。

---

## 项目结构

```
qianchuan-ai-tool/
├── start.bat              # Windows 一键启动
├── start.sh               # Mac/Linux 一键启动
├── launcher.py            # Python 启动器
├── build_exe.py           # EXE 打包脚本
├── backend/               # FastAPI 后端
│   ├── app/
│   │   ├── main.py        # 主入口（本地模式自动托管前端）
│   │   ├── api/           # API路由
│   │   ├── services/      # 业务逻辑
│   │   └── models/        # 数据模型
│   ├── requirements.txt
│   └── .env.example       # 配置模板
├── frontend/              # Vue3 单页前端
│   ├── index.html
│   ├── config.js          # 本地版配置（默认）
│   ├── config.local.js    # 本地版配置备份
│   └── config.server.js   # 服务器版配置模板
└── deploy/                # 云服务器部署方案
    └── DEPLOY.md
```

---

## 切换到服务器版

```bash
cp frontend/config.server.js frontend/config.js
# 编辑域名
vim frontend/config.js
```

详细部署指南见 `deploy/DEPLOY.md`

---

## 常见问题

### Q: 双击 start.bat 闪退？
A: Python 未安装或未添加到环境变量。运行 `python --version` 确认。

### Q: 依赖安装失败？
A: 检查网络连接，或使用国内镜像：`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt`

### Q: 启动后浏览器打不开？
A: 手动访问 http://localhost:8000

### Q: 授权失败？
A: 确保回调地址与开放平台配置一致：`http://localhost:8000/api/v1/auth/callback`

### Q: 随心推功能无法使用？
A: 需要在开放平台单独申请"随心推投放管理"和"随心推数据报表"权限。

---

GitHub: https://github.com/tkkgkv4crz-ui/qianchuan-ai-tool
