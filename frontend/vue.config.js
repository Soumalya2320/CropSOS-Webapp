const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    proxy: {
      '/predict': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/alerts': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/history': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/feedback': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/register': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/login': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
    }
  }

})
