// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true
// })

// module.exports = {
//   // publicPath: process.env.NODE_ENV == 'production' ? './' : '/',
//   publicPath:  '/', //to allow vue find the static resources
//   outputDir:'dist',
//   assetsDir:'static',


  // devServer: {
  //     proxy: {
  //         '/api': {
  //             target: 'http://127.0.0.1:8000',// 你要请求的后端接口ip+port
  //             changeOrigin: true,// 允许跨域，在本地会创建一个虚拟服务端，然后发送请求的数据，并同时接收请求的数据，这样服务端和服务端进行数据的交互就不会有跨域问题
  //             ws: true,// 开启webSocket
  //             pathRewrite: {
  //                 '^/api': '',// 替换成target中的地址
  //             }
  //         }
  //     }
  // }
// }

//------------------------------------------------------------------------

const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    publicPath: "http://127.0.0.1:8080/",
    outputDir: "./dist/",

    chainWebpack: config => {
        config.optimization.splitChunks(false)

        config.plugin('BundleTracker').use(BundleTracker, [
            {
                filename: './webpack-stats.json'
            }
        ])

        config.resolve.alias.set('__STATIC__', 'static')

        config.devServer
            .host('0.0.0.0')
            .port(8080)
            .https(false)
            .headers({'Access-Control-Allow-Origin': ['\*']})
    }
};