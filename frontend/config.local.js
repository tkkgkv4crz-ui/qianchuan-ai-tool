// 千川AI投放工具 - 本地开发版本配置
// 使用方式: 将本文件重命名为 config.js，前端即可自动加载
window.APP_CONFIG = {
    API_BASE_URL: 'http://localhost:8000',
    ENV: 'local',
    DEBUG: true
};
console.log('[千川AI工具] 当前模式: 本地开发版, API地址:', window.APP_CONFIG.API_BASE_URL);
