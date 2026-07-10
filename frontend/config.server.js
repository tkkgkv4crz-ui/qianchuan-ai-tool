// 千川AI投放工具 - 云服务器版本配置
// 使用方式:
// 1. 将域名 https://your-domain.com 替换为你的实际域名
// 2. 将本文件重命名为 config.js，替换前端目录中的本地版 config.js
// 3. 确保后端已部署到对应域名

window.APP_CONFIG = {
    API_BASE_URL: 'https://your-domain.com',
    ENV: 'production',
    DEBUG: false
};
console.log('[千川AI工具] 当前模式: 云服务器版, API地址:', window.APP_CONFIG.API_BASE_URL);
