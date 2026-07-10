// 千川AI投放工具 - 配置文件
// 默认使用本地开发版配置，部署到云服务器时请替换为 config.server.js 的内容

// ============================================
// 本地开发版（默认）- 开发调试时使用
// ============================================
window.APP_CONFIG = {
    API_BASE_URL: 'http://localhost:8000',
    ENV: 'local',
    DEBUG: true
};

// ============================================
// 云服务器版 - 部署到云服务器时使用
// 请将上方配置注释掉，取消下方注释，并替换域名
// ============================================
// window.APP_CONFIG = {
//     API_BASE_URL: 'https://your-domain.com',
//     ENV: 'production',
//     DEBUG: false
// };

console.log('[千川AI工具] 当前模式:', window.APP_CONFIG.ENV === 'local' ? '本地开发版' : '云服务器版', '| API地址:', window.APP_CONFIG.API_BASE_URL);
