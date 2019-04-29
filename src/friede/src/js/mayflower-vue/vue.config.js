module.exports = {
  chainWebpack: config => {
    config.output.chunkFilename( '[name].js' )
    if( config.plugins.has('extract-css') ) {
      const extractCSSPlugin = config.plugin('extract-css')
      extractCSSPlugin && extractCSSPlugin.tap(() => [{
        filename: '[name].css',
        chunkFilename: '[name].css'
      }])
    }
    config.optimization.splitChunks({
      cacheGroups: {
	vendors: {
          name:'vendor',
	  test: /[\\/]node_modules[\\/]/,
	  chunks: "all",
	  priority: 1
	}
      }
    });
  },
  publicPath: '/static/friede/mayflower/',
  outputDir: undefined,
  assetsDir: undefined,
  runtimeCompiler: undefined,
  productionSourceMap: undefined,
  parallel: undefined,

  css: {
    extract: true,
    sourceMap: true
  },

  lintOnSave: undefined,

  configureWebpack: {
    devtool: 'source-map'
  }
}
