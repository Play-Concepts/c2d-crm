const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = (app) => {
    app.use('/auth/callback',
        createProxyMiddleware({
            target: 'http://localhost:21188',
            secure: false,
        })
    );
};