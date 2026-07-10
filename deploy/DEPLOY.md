# 千川AI投放工具 - 云服务器部署指南

## 一、准备工作

### 1. 服务器要求
- **系统**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- **内存**: 最低 1GB，建议 2GB+
- **硬盘**: 最低 10GB
- **域名**: 建议配置域名（用于SSL证书）
- **端口**: 80, 443（对外），8000（内部API）

### 2. 千川开放平台准备
1. 注册千川开放平台账号：https://open.oceanengine.com/
2. 创建应用，获取 `AppID` 和 `AppSecret`
3. 申请以下权限：
   - 千川PC全域投放
   - 广告投放管理
   - 数据报表
   - 素材管理
   - **随心推投放管理**（需要单独申请）
   - **随心推数据报表**（需要单独申请）
4. **回调地址配置**（重要）：授权回调地址必须是HTTPS
   - 格式: `https://你的域名/api/v1/auth/callback`

> ⚠️ **随心推权限说明**：随心推 API 是独立于标准推广的另一套接口体系，需要在开放平台单独申请权限。

---

## 二、部署方式

### 方式一：一键脚本部署（推荐）

```bash
# 1. 将项目上传到服务器
scp -r qianchuan-ai-tool root@你的服务器IP:/root/

# 2. SSH登录服务器
ssh root@你的服务器IP

# 3. 修改部署脚本中的配置
cd /root/qianchuan-ai-tool/deploy
vim deploy.sh
# 修改以下变量：
# DOMAIN="your-domain.com"
# APP_ID="your_app_id"
# APP_SECRET="your_app_secret"
# EMAIL="your-email@example.com"

# 4. 运行部署脚本
chmod +x deploy.sh
./deploy.sh
```

### 方式二：Docker部署

```bash
cd qianchuan-ai-tool/deploy

# 创建环境变量文件
cat > .env << EOF
QC_APP_ID=your_app_id
QC_APP_SECRET=your_app_secret
QC_REDIRECT_URI=https://your-domain.com/api/v1/auth/callback
EOF

# 创建数据目录
mkdir -p data logs/ssl

# 启动服务
docker-compose -f docker-compose.prod.yml up -d
```

### 方式三：手动部署

```bash
# 安装依赖
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx git

# 部署后端
sudo mkdir -p /var/www/qianchuan-ai
sudo cp -r backend /var/www/qianchuan-ai/
cd /var/www/qianchuan-ai/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 部署前端
sudo cp -r frontend /var/www/qianchuan-ai/

# 配置Nginx
sudo cp deploy/nginx.conf /etc/nginx/sites-available/qianchuan-ai
sudo ln -s /etc/nginx/sites-available/qianchuan-ai /etc/nginx/sites-enabled/

# 配置Systemd
sudo cp deploy/qianchuan-ai.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable qianchuan-ai
sudo systemctl start qianchuan-ai
```

---

## 三、SSL证书配置

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 四、前端版本切换

### 模式一：本地开发版（默认）

```bash
# 启动后端（本地8000端口）
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 前端直接浏览器打开 frontend/index.html
```

### 模式二：云服务器版

```bash
cp frontend/config.server.js frontend/config.js
# 编辑域名
vim frontend/config.js
```

### 配置文件说明

| 文件 | 用途 |
|------|------|
| `config.js` | 当前生效的配置（默认本地版） |
| `config.local.js` | 本地开发版配置备份 |
| `config.server.js` | 云服务器版配置模板 |

---

## 五、备选方式：直接修改代码

如果配置文件方式无法满足需求，也可以直接修改前端代码中的API地址（约第1332行）：

```javascript
const api = axios.create({
    baseURL: 'https://your-domain.com',
    timeout: 30000
});
```

---

## 六、服务管理

```bash
sudo systemctl status qianchuan-ai
sudo systemctl start qianchuan-ai
sudo systemctl stop qianchuan-ai
sudo systemctl restart qianchuan-ai
sudo journalctl -u qianchuan-ai -f
```

---

## 七、常见问题

### Q: 授权回调失败？
A: 确保回调地址与千川开放平台配置一致，且是HTTPS。

### Q: API返回401？
A: Token已过期，调用刷新Token接口或重新授权。

### Q: Docker部署后无法访问？
A: 检查防火墙是否开放端口，以及容器是否正常运行。

### Q: 随心推API返回权限不足？
A: 随心推需要单独申请权限，确认在开放平台已申请"随心推投放管理"和"随心推数据报表"权限。

### Q: 随心推创建订单失败提示视频不可用？
A: 视频ID必须是已发布的抖音视频，且需要通过可投视频接口获取。

### Q: 批量创建随心推订单部分失败？
A: 批量创建时各订单间有1秒间隔，若视频ID无效或预算低于100元会失败。
