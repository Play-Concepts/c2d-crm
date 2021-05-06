const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = (app) => {
    app.use('/auth/callback',
        createProxyMiddleware({
            target: 'http://localhost:8000',
            secure: false,
        })
    );
};